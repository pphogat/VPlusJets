/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "alphaFunction.h" 
#include "RooAbsReal.h" 
#include "RooArgSet.h"
#include <math.h> 
#include "TMath.h" 

ClassImp(alphaFunction) 

 alphaFunction::alphaFunction(const char *name, const char *title, 
			      RooAbsReal& _x,
			      RooAbsReal& _sideband,
			      RooAbsReal& _signal) :
  RooAbsReal(name,title), 
  x("x","x",this,_x),
  sideband("sideband","sideband",this,_sideband),
  signal("signal","signal",this,_signal)
 { 
 } 


 alphaFunction::alphaFunction(const alphaFunction& other, const char* name) :  
   RooAbsReal(other,name), 
   x("x",this,other.x),
   sideband("sideband",this,other.sideband),
   signal("signal",this,other.signal)
 { 
 } 



 Double_t alphaFunction::evaluate() const 
 { 
   // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
   return signal.arg().getVal(x.arg())/sideband.arg().getVal(x.arg()) ; 
 } 
