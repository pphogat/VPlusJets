/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "RooTH1DPdf.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

ClassImp(RooTH1DPdf) 

 RooTH1DPdf::RooTH1DPdf(const char *name, const char *title, 
                        RooAbsReal& _x,
			TH1D& _hist, bool _interpolate) :
   RooAbsPdf(name,title), 
   x("x","x",this,_x),
  hist(_hist),
  interpolate(_interpolate)
 { 
   hist.SetDirectory(0);
 } 


 RooTH1DPdf::RooTH1DPdf(const RooTH1DPdf& other, const char* name) :  
   RooAbsPdf(other,name), 
   x("x",this,other.x),
   hist(other.hist),
   interpolate(other.interpolate)
 { 
   hist.SetDirectory(0);
 } 



 Double_t RooTH1DPdf::evaluate() const 
 { 
   if (interpolate)
     return TMath::Max(hist.Interpolate(x), 0.);
   else
     return TMath::Max(hist.GetBinContent(hist.FindBin(x)), 0.);
 }



 Int_t RooTH1DPdf::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* /*rangeName*/) const  
 { 
   // LIST HERE OVER WHICH VARIABLES ANALYTICAL INTEGRATION IS SUPPORTED, 
   // ASSIGN A NUMERIC CODE FOR EACH SUPPORTED (SET OF) PARAMETERS 
   // THE EXAMPLE BELOW ASSIGNS CODE 1 TO INTEGRATION OVER VARIABLE X
   // YOU CAN ALSO IMPLEMENT MORE THAN ONE ANALYTICAL INTEGRAL BY REPEATING THE matchArgs 
   // EXPRESSION MULTIPLE TIMES

   if (matchArgs(allVars,analVars,x)) return 1 ; 
   return 0 ; 
 } 



 Double_t RooTH1DPdf::analyticalIntegral(Int_t code, const char* rangeName) const  
 { 
   // RETURN ANALYTICAL INTEGRAL DEFINED BY RETURN CODE ASSIGNED BY getAnalyticalIntegral
   // THE MEMBER FUNCTION x.min(rangeName) AND x.max(rangeName) WILL RETURN THE INTEGRATION
   // BOUNDARIES FOR EACH OBSERVABLE x

   if (code==1) {
     
     return hist.Integral(hist.FindBin(x.min(rangeName)), 
			  hist.FindBin(x.max(rangeName)), "width");
   } 
   return 0 ; 
 } 
