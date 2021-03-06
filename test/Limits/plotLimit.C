//root -b -q -l upperLimit.C+
#include <iostream>

#include "TGraph.h"
#include "TGraphAsymmErrors.h"
#include "TMultiGraph.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TLegend.h"
#include "TText.h"
#include "TLatex.h"
#include "TAxis.h"
#include "TLine.h"
#include "TH1F.h"
#include "TString.h"

#include "tdrstyle.C"

#include "hwwinputs.h"

//#define LOGY

//#define ADD7TEV
#undef ADD7TEV

#define YMAX 20.0

//======================================================================

////CMS Preliminary label and lumi -- upper left corner
void cmsLumi(bool prelim)
{
  //const float LUMINOSITY = intlumipbinv_el * global_scale/1000.;
  const float LUMINOSITY = 5.1; // 5.2;
  //const float LUMINOSITY = 10.1;
  TLatex latex;
  latex.SetNDC();
  latex.SetTextSize(0.04);
  latex.SetTextFont(42);

#ifdef ADD7TEV
  float lumiel=intlumipbinv_el+5020;
  float lumimu=intlumipbinv_mu+5020;
  //float lumiel=LUMINOSITY*1000+5020;
  //float lumimu=LUMINOSITY*1000+5020;
#else
  float lumiel=intlumipbinv_el;
  float lumimu=intlumipbinv_mu;
#endif

  latex.SetTextAlign(31); // align right

#ifdef ADD7TEV
  latex.DrawLatex(0.95,0.96,"#sqrt{s} = 7TeV/8TeV");
#else
  latex.DrawLatex(0.90,0.96,Form("#sqrt{s} = %d TeV",beamcomenergytev));
#endif

  if (LUMINOSITY > 0.) {
    latex.SetTextAlign(11); // align left
#if 1
    if (lumiel==lumimu)
      latex.DrawLatex(0.5,0.96,Form("#scale[0.5]{#int} #font[12]{L} dt = %.1f fb^{-1}", lumiel/1000.));
    else
      latex.DrawLatex(0.4,0.96,Form("#scale[0.5]{#int} #font[12]{L} dt = %.1f fb^{-1}(#mu)/%.1f fb^{-1}(#it{e})",
				    (lumimu)/1000.,(lumiel)/1000.));
#else
    latex.DrawLatex(0.4,0.96,Form("#scale[0.5]{#int} #font[12]{L} dt = %.1f fb^{-1}(#it{e})",lumiel/1000.));
    //latex.DrawLatex(0.4,0.96,Form("#scale[0.5]{#int} #font[12]{L} dt = %.1f fb^{-1}(#mu)",lumimu/1000.));
#endif
    //latex.DrawLatex(0.45,0.96,Form("#scale[0.5]{#int} #font[12]{L} dt = %.1f fb^{-1} (scaled)", LUMINOSITY));
  }
  latex.SetTextAlign(11); // align left
  latex.DrawLatex(0.18,0.96,prelim ? "CMS preliminary" : "CMS");
}

//======================================================================

void plotLimit(TString limitFile = "limit-cfginfo.tab",
	       bool plotObs = true,
	       bool plotPrelim=true)
{
  double m[100],obs[100],exp[100],sig1hi[100],sig1lo[100],sig2hi[100],sig2lo[100];
  char line[256];

  FILE *fp=fopen(limitFile.Data(),"r");
  if (!fp) {
    cerr << limitFile << " doesn't exist." << endl;
    exit(-1);
  }
  int npts=0;
  for (int i=0; !feof(fp) && fgets(line,256,fp); ) {
    if (line[0]=='#') continue;
    int nread = sscanf(line,"%lf %lf %lf %lf %lf %lf %lf",
		       &m[i],&obs[i],&sig2lo[i],&sig1lo[i],&exp[i],&sig1hi[i],&sig2hi[i]);

    if (nread == 0) continue;
    else if (nread == 7) {
      sig1hi[i] -= exp[i];
      sig1lo[i] = exp[i]-sig1lo[i];
      sig2hi[i] -= exp[i];
      sig2lo[i] = exp[i]-sig2lo[i];
      i++; npts=i;
    }
  }
  fclose(fp);

  cout << "Read " << npts << " points." << endl;

  TGraph *obslim=new TGraph(npts,m,obs); // obslim->Print();
  TGraph *explim=new TGraph(npts,m,exp); // explim->Print();
  TGraphAsymmErrors *exp1sig=new TGraphAsymmErrors(npts,m,exp,0,0,sig1lo,sig1hi);
  TGraphAsymmErrors *exp2sig=new TGraphAsymmErrors(npts,m,exp,0,0,sig2lo,sig2hi);

  setTDRStyle();

  gStyle->SetLegendBorderSize(0);

  // Style for lines
  explim->SetLineWidth(3);
  explim->SetLineStyle(2);
  obslim->SetLineWidth(3);
  obslim->SetLineColor(1);
  obslim->SetLineStyle(1);
  exp1sig->SetFillColor(kGreen); // kBlue - 7);
  exp2sig->SetFillColor(kYellow);

  TMultiGraph* mg = new TMultiGraph();
  mg->SetName("");
  mg->SetTitle(";M_{H} (GeV);#sigma_{excluded} / #sigma_{SM}"); // (gg #rightarrow H #rightarrow WW #rightarrow #ell#nujj)");

  mg->Add(exp2sig, "E3");
  mg->Add(exp1sig, "E3");
  mg->Add(explim, "L");
  if (plotObs)
    mg->Add(obslim, "L");

  mg->Draw("AH");
  //mg->GetXaxis()->SetRangeUser(0., double(npts));

#ifdef LOGY
  mg->GetYaxis()->SetRangeUser(5e-2,40) ;
#else
  mg->GetYaxis()->SetRangeUser(0,YMAX) ;
#endif

  //mg->Draw("A");

  TLine l;
  l.SetLineWidth(2);
  l.SetLineColor(2);
  l.DrawLine(mg->GetXaxis()->GetXmin(),1.0,mg->GetXaxis()->GetXmax(),1.0);


  gPad->SetGridy();

#ifdef LOGY
  gPad->SetLogy();
#endif

  mg->GetHistogram()->DrawCopy("sameaxis");
  mg->GetHistogram()->DrawCopy("sameaxig");

  TLegend *leg = new TLegend(0.38, 0.77, 0.75, 0.94, NULL, "brNDC");
  leg->SetTextSize(0.04);
  leg->SetTextFont(42);
  leg->SetFillColor(0);
  if (plotObs)
    leg->AddEntry(obslim, "95% C.L. Observed Limit", "L");
  leg->AddEntry(explim, "95% C.L. Expected Limit", "L");
  leg->AddEntry(exp1sig, "#pm1#sigma Expected Limit", "F");
  leg->AddEntry(exp2sig, "#pm2#sigma Expected Limit", "F");
  leg->Draw();

  cmsLumi(plotPrelim);

  gPad->Update();
}

//======================================================================

void plotLimit2(TString limitFile = "limit-cfginfo.tab",
		bool plotObs = true,
		bool plotPrelim=true)
{
  TCanvas *c1 = new TCanvas("c1","c1",800,600);

  plotLimit(limitFile,plotObs,plotPrelim);

  TString output1=limitFile, output2=limitFile;

  output1.Replace(limitFile.Length()-4,4, plotObs ? ".png" : "_exponly.png");
  output2.Replace(limitFile.Length()-4,4, plotObs ? ".eps" : "_exponly.eps");

  gPad->SaveAs(output1.Data());
  gPad->SaveAs(output2.Data());

}
