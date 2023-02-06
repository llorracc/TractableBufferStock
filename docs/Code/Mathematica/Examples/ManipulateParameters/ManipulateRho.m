(* ::Package:: *)

(************************************************************************)
(* This file was generated automatically by the Mathematica front end.  *)
(* It contains Initialization cells from a Notebook file, which         *)
(* typically will have the same name as this file except ending in      *)
(* ".nb" instead of ".m".                                               *)
(*                                                                      *)
(* This file is intended to be loaded into the Mathematica kernel using *)
(* the package loading commands Get or Needs.  Doing so is equivalent   *)
(* to using the Evaluate Initialization Cells menu command in the front *)
(* end.                                                                 *)
(*                                                                      *)
(* DO NOT EDIT THIS FILE.  This entire file is regenerated              *)
(* automatically each time the parent Notebook file is saved in the     *)
(* Mathematica front end.  Any changes you make to this file will be    *)
(* overwritten.                                                         *)
(************************************************************************)



SetDirectory[NotebookDirectory[]];<<ManipulatePrepare.m;FindStableArm;
{\[ScriptM]Max,\[ScriptM]MaxMax}={3,10} \[ScriptM]E;\[ScriptC]Max=cE[\[ScriptM]Max];
Manipulate[
Block[{$PerformanceGoal="Quality",\[Rho],\[Rho]Base},\[Rho]=\[Rho]Base=2.5;{\[ScriptM]Max,\[ScriptM]MaxMax}={2,5}\[ScriptM]E;
\[Rho]=\[Rho]Slider;If[((R) \[Beta])^(1/\[Rho])/\[CapitalGamma] >=  1||((R) \[Beta])^(1/\[Rho])/(R) >=  1,Style[Text["Impatience Condition Not Satisfied."],24]];
DrawPhaseDiagram[\[ScriptM]Max,\[ScriptM]MaxMax,\[ScriptC]Max]
],{{\[Rho]Slider,2.5,"\[Rho]"},1.001,4.001,0.25}]



