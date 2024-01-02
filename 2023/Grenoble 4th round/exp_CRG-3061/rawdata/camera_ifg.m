(* ::Package:: *)

BeginPackage["CameraIfgPackage`"]

loadimage::usage="import multi-page TIFF file"
cut::usage="cut out a tile"
binimage::usage="make binning"
getfitdata::usage="create interferogram from tile"
fit::usage="fit an interferogram"
plotfit::usage="show data and fit"
plotfitxy::usage="show data and fit"
fitifg::usage="fit interferogram"
fitarea::usage="cut and fit area"
fittile::usage="cut and fit tile"
fitgrid::usage="cut and fit all tiles"
showtileres::usage="[res,nx,ny] show results and plot of a tile fit; nx,ny from 0"
showareares::usage="show results and plot of an area fit"
plotres::usage="density plots of results over beam profile"
plotvsslot::usage="plot contrast, phase etc. vs slot no"
contrast::usage="contrast of single tile"
offset::usage="offset of single tile"
period::usage="period of single tile"
phase::usage="phase of single tile"

(* for Gauss fit: *)
fitGauss::usage="fit a double Gaussian"
fitareaGauss::usage="cut and fit area"
fittileGauss::usage="cut and fit tile"
fitgridGauss::usage="cut and fit all tiles"
plotresGauss::usage="show density plot"
showtileresGauss::usage="[res,nx,ny] show results and plot of a tile fit; nx,ny from 0"

(* for double Gauss fit: *)
peakheight::usage="peak height of single tile"
peakpos::usage="peak position of single tile"
peakwidth::usage="peak width of single tile"
peaksep::usage="peak separation of single tile"
fitTwoGauss::usage="fit a double Gaussian"
fitareaTwoGauss::usage="cut and fit area"
fittileTwoGauss::usage="cut and fit tile"
fitgridTwoGauss::usage="cut and fit all tiles"
showtileresTwoGauss::usage="[res,nx,ny] show results and plot of a tile fit; nx,ny from 0"
showarearesTwoGauss::usage="show results and plot of an area fit"
plotresTwoGauss::usage="density plots of Two-Gauss-Fit results"


Begin["`Private`"]

loadimage[name_]:=Module[{imp},imp=Import[name,"Data"]; If[Length[Dimensions[imp]]==3,imp,{imp}]]
cutarea[images_,x_,y_,dx_,dy_]      :=Table[Take[  Take[#,{x+1,x+dx} ]& /@ images[[n]]   , {y+1,y+dy}],{n,1,Length[images]}]
(* cutarea: x,y count from 0 *)
cut[images_,tileDX_,tileDY_,nx_,ny_]:=Table[Take[  Take[#,{(ny-1)*tileDX+1,ny*tileDX} ]& /@ images[[n]]   , {(nx-1)*tileDY+1,nx*tileDY}],{n,1,Length[images]}]
getfitdata[data_]:=Total[#,2]&  /@  data

binimage[img_,dx_,dy_]:=Module[{xmax,ymax},
xmax=Floor[Length[img[[1]]]/dx];ymax=Floor[Length[img]/dy];
Table[Table[Total[Take[ #,{x,x+dx-1}]&/@   Take[img,{y,y+dy-1} ] ,2] ,{x,1,dx*xmax,dx}],{y,1,dy*ymax,dy}]]

fit[fitdata_,period_]:=Module[{result},  (* period<0 means: assume fixed period *)
result=If[period<0,
NonlinearModelFit[fitdata, {a+Abs[b]*Sin[-2\[Pi]*x/period+d]},{{a,Mean[fitdata]},{b,(Max[fitdata]-Min[fitdata])/2},{d,0}},x, AccuracyGoal->5, Weights->(Sqrt[#2]&)]
(*NonlinearModelFit[fitdata, {a+Abs[b]*Sin[c*x+d],c\[Equal]-2\[Pi]/period},{{a,Mean[fitdata]},{b,(Max[fitdata]-Min[fitdata])/2},{c,-2\[Pi]/period},{d,0}},x, AccuracyGoal->5, Weights->(Sqrt[#2]&)]*),
NonlinearModelFit[fitdata, a+Abs[b]*Sin[c*x+d],{{a,Mean[fitdata]},{b,(Max[fitdata]-Min[fitdata])/2},{c,2\[Pi]/period},{d,0}},x, AccuracyGoal->5, Weights->(Sqrt[#2]&)]];
(* falls nicht konvergiert (amplitude\[Equal]0) dann mit Fitstartwert f\[UDoubleDot]r Phase um 180 \[ADoubleDot]ndern und nochmal probieren *)
result = If[Abs[result["ParameterTableEntries"][[2,1]]] > 1, result, 
If[period<0,
NonlinearModelFit[fitdata, {a+Abs[b]*Sin[-2\[Pi]*x/period+d]},{{a,Mean[fitdata]},{b,(Max[fitdata]-Min[fitdata])/2},{d,\[Pi]}},x, AccuracyGoal->5, Weights->(Sqrt[#2]&)],
NonlinearModelFit[fitdata, a+Abs[b]*Sin[c*x+d],{{a,Mean[fitdata]},{b,(Max[fitdata]-Min[fitdata])/2},{c,2\[Pi]/period},{d,\[Pi]}},x, AccuracyGoal->5, Weights->(Sqrt[#2]&)]]   ];
result
]
contr[fit_]:=Abs[fit["ParameterTableEntries"][[2,1]]/fit["ParameterTableEntries"][[1,1]]];
plotfit[fitdata_,fitresult_]:=Show[{ListPlot[fitdata],Plot[fitresult[x],{x,1,Length[fitdata]}]},ImageSize->300,AxesLabel->{"image no","counts"},PlotRange->{0,Automatic}];
plotfitxy[fitdata_,fitresult_]:=Show[{ListPlot[fitdata],Plot[fitresult[x],{x,fitdata[[1,1]],fitdata[[Length[fitdata],1]]}]},ImageSize->300,AxesLabel->{"","counts"},PlotRange->{0,Max[Transpose[fitdata][[2]]]}];


fitifg[fitdata_, minIntensity_,period_]:=Module[{fitres,totalIntensity, c,offs,ampl,per,phdeg},
totalIntensity=Total[fitdata];
(*minIntensity=50;*)
fitres=If[ totalIntensity>minIntensity, fit[fitdata,period],{}];
c=If[ totalIntensity>minIntensity,contr[fitres],NaN];
offs=Max[0,If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[1,1]],NaN]];
ampl=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[2,1]],NaN];
per=If[period<0,Abs[period],If[ totalIntensity>minIntensity,2\[Pi]/fitres["ParameterTableEntries"][[3,1]],NaN]];
phdeg=If[ totalIntensity>minIntensity,  Mod[(fitres["ParameterTableEntries"][[If[period<0,3,4],1]]*180/(\[Pi]) + If[fitres["ParameterTableEntries"][[2,1]]>=0,0,180]),360]  ,NaN];
phdeg=If[ totalIntensity>minIntensity,Mod[If[ampl<0,180+phdeg,phdeg]+3600,360] ,NaN];
{fitdata,fitres,c,offs,per,phdeg,  
Abs[period]} (* keep period start value for plot scale range *)
]

fitarea[images_,x_,y_,dx_,dy_,minIntensity_,period_]:=Module[{ imgdata},
(*imgdata=cut[images,tileDX,tileDY,nx,ny];*)
imgdata=cutarea[images,x,y,dx,dy];
fitdata=getfitdata[imgdata];
fitifg[fitdata,minIntensity,period]
]

fittile[images_,tileDX_,tileDY_,nx_,ny_,minIntensity_,period_]:=Module[{},
fitarea[images,(nx-1)*tileDX,(ny-1)*tileDY,tileDX,tileDY,minIntensity,period]
]

fitgrid[images_,tileDX_,tileDY_,minIntensity_,period_]:=Module[{},
Table[fittile[images,tileDX,tileDY,nx,ny,minIntensity,period],{ny,1,Floor[Length[images[[1]]]/tileDY]},{nx,1,Floor[Length[images[[1,1]]]/tileDX]}]
]

plotvsslot[slotres_]:=Row[{ListPlot[Transpose[slotres][[3]],ImageSize->300,AxesLabel->{"slot","contrast"},PlotRange->{0,1}], 
ListPlot[Transpose[slotres][[6]],ImageSize->300,AxesLabel->{"slot","phase"},PlotRange->{0,365}]
}]


showtileres[res_,nx_,ny_]:=Module[{},  (* nx,ny ab 0 *)
showareares[res[[ny+1,nx+1]]]
]

showareares[res_]:=Module[{fitdata,fitres},
fitdata=res[[1]];
fitres=res[[2]];
Row[{plotfit[fitdata,fitres],res[[2]]["ParameterTable"],
Column[{"contr="<>ToString[res[[3]]], "offs="<>ToString[res[[4]]], "phase="<>ToString[res[[6]]]<>"\[Degree]", "period="<>ToString[res[[5]]]}]},"    " ]
]

contrast[res_,x_,y_]:=res[[y-1,x-1,3]];
offset[res_,x_,y_]:=res[[y-1,x-1,4]];
period[res_,x_,y_]:=res[[y-1,x-1,5]];
phase[res_,x_,y_]:=res[[y-1,x-1,6]];




(* ********************************************************** *)
(*                    Gauss Fit                           *)
(* ********************************************************** *)

(* ignorebelow: ignore data points with values below this fraction of the peak value *)
fitGauss[fitdata_,ignorebelow_]:=Module[{maxy,xmaxy,sig,fd},
maxy= If[ArrayDepth[fitdata]==1,Max[fitdata],                 Max[Transpose[fitdata][[2]]]];
xmaxy=If[ArrayDepth[fitdata]==1,FirstPosition[fitdata,maxy][[1]],  fitdata[[ FirstPosition[Transpose[fitdata][[2]],maxy][[1]], 1]] ];
sig=  If[ArrayDepth[fitdata]==1,Length[fitdata]/10,      (fitdata[[Length[fitdata],1]]-fitdata[[1,1]])/10];
fd=If[ignorebelow==0,fitdata, Select[fitdata, If[ArrayDepth[fitdata]==1, #>=maxy*ignorebelow &,  #[[2]] >= maxy*ignorebelow&]  ]];
NonlinearModelFit[fd, b*(Exp[-(x-c)^2/(2 d^2)]),{{b,maxy},{c,xmaxy},{d,sig}},x]
]

fitareaGauss[images_,xaxis_,x_,y_,dx_,dy_,minIntensity_,ignorebelow_]:=Module[{ imgdata,fitdata,fitres,totalIntensity, c,offs,ampl,pos,sig,fwhm},
(*imgdata=cut[images,tileDX,tileDY,nx,ny];*)
imgdata=cutarea[images,x,y,dx,dy];
fitdata=getfitdata[imgdata];
totalIntensity=If[ArrayDepth[fitdata]==1,Total[fitdata],Total[Transpose[fitdata][[2]]]];
fitdata=If[Length[fitdata]==Length[xaxis],Transpose[{xaxis,fitdata}],fitdata];
fitres=If[ totalIntensity>minIntensity, fitGauss[fitdata,ignorebelow],{}];
ampl=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[1,1]],NaN];
pos=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[2,1]],NaN];
sig=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[3,1]],NaN];
fwhm=sig*2/Sqrt[Log[2]];
{fitdata,fitres,ampl,pos,Abs[sig],Abs[fwhm]}
]

fittileGauss[images_,xaxis_,tileDX_,tileDY_,nx_,ny_,minIntensity_,ignorebelow_]:=Module[{},
fitareaGauss[images,xaxis,(nx-1)*tileDX,(ny-1)*tileDY,tileDX,tileDY,minIntensity,ignorebelow]
]

fitgridGauss[images_,xaxis_,tileDX_,tileDY_,minIntensity_,ignorebelow_]:=Module[{},
Table[fittileGauss[images,xaxis,tileDX,tileDY,nx,ny,minIntensity,ignorebelow],{ny,1,Floor[Length[images[[1]]]/tileDY]},{nx,1,Floor[Length[images[[1,1]]]/tileDX]}]
]

fwhmTable[res_]:=res[[All,All,6]]
posTable[res_]:=res[[All,All,4]]
intensTable[res_]:=res[[All,All,3]]
fwhmColFunc[v_,mn_,mx_]:=ColorData["BlueGreenYellow"][(v-mn)/(mx-mn)];
posColFunc[v_,mn_,mx_]:=ColorData["LightTemperatureMap"][(v-mn)/(mx-mn)];
intensColFunc[v_,mn_,mx_]:=ColorData["GrayTones"][(v-mn)/(mx-mn)];

plotresGauss[res_,imgsize_,dfwhm_,dpos_]:=Module[{intens1,intensmin,intensmax,fwhm1,fwhmmean,fwhmmin,fwhmmax,pos1,posmean,posmin,posmax},
intens1=intensTable[res];   intensmin=0; intensmax=Max[intens1];
fwhm1=fwhmTable[res];       fwhmmean=Abs[(Min[fwhm1]+Max[fwhm1])/2];  fwhmmin=fwhmmean-dfwhm; fwhmmax=fwhmmean+dfwhm;
pos1=posTable[res];         posmean=(Min[pos1]+Max[pos1])/2;  posmin=posmean-dpos; posmax=posmean+dpos;
Row[{
ArrayPlot[intens1,ImageSize->imgsize,ColorFunction->(intensColFunc[#,intensmin,intensmax]&),ColorFunctionScaling->False,PlotLegends->BarLegend[{intensColFunc[#,intensmin,intensmax]&,{intensmin,intensmax}}],PlotLabel->"Intensity"],
ArrayPlot[fwhm1  ,ImageSize->imgsize,ColorFunction->(  fwhmColFunc[#,  fwhmmin,  fwhmmax]&),ColorFunctionScaling->False,PlotLegends->BarLegend[{fwhmColFunc[#,fwhmmin,fwhmmax]&,{fwhmmin,fwhmmax}}],PlotLabel->"FWHM/deg"],
ArrayPlot[pos1   ,ImageSize->imgsize,ColorFunction->(   posColFunc[#,   posmin,   posmax]&),ColorFunctionScaling->False,PlotLegends->BarLegend[{posColFunc[#,posmin,posmax]&,{posmin,posmax}}],PlotLabel->"PeakPos/deg"]}]
]
plotresGauss[res_]:=plotresGauss[res,300,1,1]

showtileresGauss[res_,nx_,ny_]:=Module[{},  (* nx,ny ab 0 *)
showarearesGauss[res[[ny+1,nx+1]]]
]
showarearesGauss[res_]:=Module[{fitdata,fitres},
fitdata=res[[1]];
fitres=res[[2]];
Row[{plotfitxy[fitdata,fitres],res[[2]]["ParameterTable"],
Column[{"peakheight="<>ToString[res[[3]]], "peakpos="<>ToString[res[[4]]], "width(sigma)="<>ToString[res[[5]]], "FWHM="<>ToString[res[[6]]]}]}]
]


(* ********************************************************** *)
(*                    Two-Gauss Fit                           *)
(* ********************************************************** *)

fitTwoGauss[fitdata_,xaxis_]:=NonlinearModelFit[Transpose[{xaxis,fitdata}], b*(Exp[-(x-c)^2/(2 d^2)]+Exp[-(x-(c+sep))^2/(2 d^2)]),{{b,Max[fitdata]},{c,xaxis[[Ceiling[Length[xaxis]/4]]]},{d,(xaxis[[Length[xaxis]]]-xaxis[[1]])/10},{sep,(xaxis[[Length[xaxis]]]-xaxis[[1]])/2}},x]

fitareaTwoGauss[images_,xaxis_,x_,y_,dx_,dy_,minIntensity_]:=Module[{ imgdata,fitdata,fitres,totalIntensity, c,offs,ampl,pos,sig,sep},
(*imgdata=cut[images,tileDX,tileDY,nx,ny];*)
imgdata=cutarea[images,x,y,dx,dy];
fitdata=getfitdata[imgdata];
totalIntensity=Total[fitdata]; 
(*minIntensity=50;*)
fitres=If[ totalIntensity>minIntensity, fitTwoGauss[fitdata,xaxis],{}];
(*offs=Max[0,If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[1,1]],NaN]];*)
ampl=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[1,1]],NaN];
pos=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[2,1]],NaN];
sig=If[ totalIntensity>minIntensity,fitres["ParameterTableEntries"][[3,1]],NaN];
sep=If[ totalIntensity>minIntensity,Abs[fitres["ParameterTableEntries"]][[4,1]],NaN];
{Transpose[{xaxis,fitdata}],fitres,ampl,pos,sig,sep}
]

fittileTwoGauss[images_,xaxis_,tileDX_,tileDY_,nx_,ny_,minIntensity_]:=Module[{},
fitareaTwoGauss[images,xaxis,(nx-1)*tileDX,(ny-1)*tileDY,tileDX,tileDY,minIntensity]
]

fitgridTwoGauss[images_,xaxis_,tileDX_,tileDY_,minIntensity_]:=Module[{},
Table[fittileTwoGauss[images,xaxis,tileDX,tileDY,nx,ny,minIntensity],{ny,1,Floor[Length[images[[1]]]/tileDY]},{nx,1,Floor[Length[images[[1,1]]]/tileDX]}]
]



showtileresTwoGauss[res_,nx_,ny_]:=Module[{},  (* nx,ny ab 0 *)
showarearesTwoGauss[res[[ny+1,nx+1]]]
]

showarearesTwoGauss[res_]:=Module[{fitdata,fitres},
fitdata=res[[1]];
fitres=res[[2]];
Row[{plotfitxy[fitdata,fitres],res[[2]]["ParameterTable"],
Column[{"peakheight="<>ToString[res[[3]]], "peakpos="<>ToString[res[[4]]], "peakwidth="<>ToString[res[[5]]], "peaksep="<>ToString[res[[6]]]}]}]
]

peakheight[res_,x_,y_]:=res[[y+1,x+1,3]];
(*offset[res_,x_,y_]:=res[[y+1,x+1,4]];  same as for interferogram *)  
peakpos[res_,x_,y_]:=res[[y+1,x+1,4]];
peakwidth[res_,x_,y_]:=res[[y+1,x+1,5]];
peaksep[res_,x_,y_]:=res[[y+1,x+1,6]];




contrTable[res_]:=Reverse[res[[All,All,3]],1] /. CameraIfgPackage`Private`NaN->0;
offsTable[res_]:=Reverse[res[[All,All,4]],1] /. CameraIfgPackage`Private`NaN->0;
periTable[res_]:=Reverse[res[[All,All,5]],1] ;
phaseTable[res_]:=Reverse[res[[All,All,6]],1]/. CameraIfgPackage`Private`NaN->0;

contrColFunc[v_]:=If[v==0 || v==CameraIfgPackage`Private`NaN,White,ColorData["DarkBands"][(1-v)*5/6]];
contrColFunc[v_]:=If[v==0,White,ColorData["CMYKColors"][(1-v)]];
phaseColFunc[v_]:=Hue[v+0.02 Sin[6 \[Pi] v],0.9,0.95]; (* der Sinusterm macht die Bereiche Y,C,M etwas breiter gegen\[UDoubleDot]ber R,G,B *)

plotres[res_]:=plotres[res,180];

plotres[res_,imgsize_]:=Module[{drx,dry,prx,pry,intens,isize,ar,lst,peri},
drx={0.5,Dimensions[res][[2]]-0.5};  (* data range = image dimension in units of the scales on the axes *)
dry={0.5,Dimensions[res][[1]]-0.5}; 
prx={-0.3,Dimensions[res][[2]]+0.3};  (* plot range = range of scale on the axes *)
pry={-0.3,Dimensions[res][[1]]+0.3};
intens=Max[Select[Flatten[offsTable[res]],NumberQ]];
isize=180;
ar=(pry[[2]]-pry[[1]])/(prx[[2]]-prx[[1]]);
(* lst=DeleteCases[Flatten[periTable[res]],CameraIfgPackage`Private`NaN];
peri=Total[lst]/Length[lst]; *)
peri=res[[1,1,7]];
Row[{
ArrayPlot[contrTable[res],DataRange->{drx,dry},PlotRange->{prx,pry,{0,1}},FrameTicks->{Automatic,Automatic},ImageSize->imgsize,AspectRatio->ar,PlotLegends->BarLegend[{contrColFunc[#]&,{0.3,0.9}}],PlotLabel->"Contrast",ColorFunction->contrColFunc,ColorFunctionScaling->False],
ArrayPlot[phaseTable[res],DataRange->{drx,dry},PlotRange->{prx,pry,{0,360}},FrameTicks->{Automatic,Automatic},ImageSize->imgsize,AspectRatio->ar,PlotLegends->BarLegend[{phaseColFunc[#]&,{0,360}}],PlotLabel->"Phase",ColorFunction->phaseColFunc],
ArrayPlot[offsTable[res],DataRange->{drx,dry},PlotRange->{prx,pry,{0,intens}},FrameTicks->{Automatic,Automatic},ImageSize->imgsize,AspectRatio->ar,PlotLegends->Automatic,PlotLabel->"Mean Intensity",ColorFunction->"GrayTones"],
ArrayPlot[periTable[res],DataRange->{drx,dry},PlotRange->{prx,pry,{peri*0.9,peri*1.1}},FrameTicks->{Automatic,Automatic},ImageSize->imgsize,AspectRatio->ar,PlotLegends->Automatic,PlotLabel->"Period",ColorFunction->"CoffeeTones"]
(*ListDensityPlot[contrTable[res],Mesh->None,MaxPlotPoints\[Rule]dim,InterpolationOrder->0,DataRange->{drx,dry},PlotRange->{prx,pry,{0,1}},ImageSize->isize,PlotLegends->Automatic,PlotLabel->"Contrast",ColorFunction->contrColFunc,ColorFunctionScaling->False],
ListDensityPlot[phaseTable[res],Mesh->None,InterpolationOrder->0,DataRange->{drx,dry},PlotRange->{prx,pry,{0,360}},ImageSize->isize,PlotLegends->Automatic,PlotLabel->"Phase",ColorFunction->phaseColFunc],
ListDensityPlot[offsTable[res],Mesh->None,InterpolationOrder->0,DataRange->{drx,dry},PlotRange->{prx,pry,{0,intens}},ImageSize->isize,PlotLegends->Automatic,PlotLabel->"Mean Intensity",ColorFunction->"GrayTones" ] ,
ListDensityPlot[periTable[res],Mesh->None,InterpolationOrder->0,DataRange->{drx,dry},PlotRange->{prx,pry,Automatic},ImageSize->isize,PlotLegends->Automatic,PlotLabel->"Period"*)
 }]
]

End[]
EndPackage[]


peakheightTable[res_]:=Reverse[res[[All,All,3]],1] /. CameraIfgPackage`Private`NaN->0;
peakposTable[res_]:=Reverse[res[[All,All,4]],1] /. CameraIfgPackage`Private`NaN->0;
peakwidthTable[res_]:=Reverse[res[[All,All,5]],1] ;
peaksepTable[res_]:=Reverse[res[[All,All,6]],1]/. CameraIfgPackage`Private`NaN->0;

contrColFunc[v_]:=If[v==0 || v==CameraIfgPackage`Private`NaN,White,ColorData["DarkBands"][(1-v)*5/6]];
contrColFunc[v_]:=If[v==0,White,ColorData["CMYKColors"][(1-v)]];
phaseColFunc[v_]:=Hue[v+0.02 Sin[6 \[Pi] v],0.9,0.95]; (* der Sinusterm macht die Bereiche Y,C,M etwas breiter gegen\[UDoubleDot]ber R,G,B *)

plotresTwoGauss[res_]:=Module[{drx,dry,prx,pry,ar},
drx={0.5,Dimensions[res][[2]]-0.5};  (* data range = image dimension in units of the scales on the axes *)
dry={0.5,Dimensions[res][[1]]-0.5}; 
prx={-0.3,Dimensions[res][[2]]+0.3};  (* plot range = range of scale on the axes *)
pry={-0.3,Dimensions[res][[1]]+0.3};
ar=(pry[[2]]-pry[[1]])/(prx[[2]]-prx[[1]]);
Row[{
ArrayPlot[peakheightTable[res]               ,DataRange->{drx,dry},PlotRange->{prx,pry,Automatic},FrameTicks->{Automatic,Automatic},ImageSize->180,AspectRatio->ar,PlotLegends->Automatic,PlotLabel->"Peak Height"],
ArrayPlot[peakposTable[res]                  ,DataRange->{drx,dry},PlotRange->{prx,pry,{res[[1,1,1,1,1]],res[[1,1,1,Length[res[[1,1,1]]],1]] }   },FrameTicks->{Automatic,Automatic},ImageSize->180,AspectRatio->ar,PlotLegends->Automatic,PlotLabel->"Peak Position",ColorFunction->"BeachColors"],
ArrayPlot[peakwidthTable[res]*2Sqrt[2 Log[2]],DataRange->{drx,dry},PlotRange->{prx,pry,Automatic},FrameTicks->{Automatic,Automatic},ImageSize->180,AspectRatio->ar,PlotLegends->Automatic,PlotLabel->"Peak Width",ColorFunction->"GrayTones"],
ArrayPlot[peaksepTable[res]                  ,DataRange->{drx,dry},PlotRange->{prx,pry,{0,Max[res[[All,All,6]]]}},FrameTicks->{Automatic,Automatic},ImageSize->180,AspectRatio->ar,PlotLegends->Automatic,PlotLabel->"Peak Separation",ColorFunction->"CoffeeTones"]
 }]
]

