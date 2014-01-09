/* -*- mode: C++ -*- *********************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROORELBWRUNNINGWIDTH
#define ROORELBWRUNNINGWIDTH

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooRelBWRunningWidth : public RooAbsPdf {
public:
  RooRelBWRunningWidth() {} ; 
  RooRelBWRunningWidth(const char *name, const char *title,
	      RooAbsReal& _mww,
	      RooAbsReal& _mH,
	      RooAbsReal& _gamma);
  RooRelBWRunningWidth(const RooRelBWRunningWidth& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooRelBWRunningWidth(*this,newname); }
  inline virtual ~RooRelBWRunningWidth() { }

protected:

  RooRealProxy mww ;
  RooRealProxy mH ;
  RooRealProxy gamma ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooRelBWRunningWidth,1) // Your description goes here...
};
 
#endif
