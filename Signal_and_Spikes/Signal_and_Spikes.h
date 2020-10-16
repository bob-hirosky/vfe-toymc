#pragma once

#include "TFile.h"
#include "TGraph.h"


class Pulse{
public:
  Pulse(int);
  ~Pulse();
  double Value(double t) { return grPulse_->Eval(t+tshift_); };
  double Xpeak() { return xpeak_; }
  double Ypeak() { return ypeak_; }
  double GetPhi() { return phi_; }
  void SetPhi(double phi) { phi_=phi; }
  void SetT0(double t=0) { tshift_= Xpeak()-t; }
  double tshift_;
  double phi_;
  double xpeak_;
  double ypeak_;
  private:
  TGraph *grPulse_;
};



Pulse::Pulse(int iopt)
{
  phi_=0;
  tshift_=0;
  TFile *file = new TFile("200626_Signal_Spike_Pulse_Shapes.root");
  if(iopt==0){ // Signal Phase 1
    grPulse_ = (TGraph*)file->Get("grSignal_Legacy");
  }else if(iopt==1){ // Spike Phase 1
    grPulse_ = (TGraph*)file->Get("grSpike_Legacy");
  }else if(iopt==2){ // Signal Phase 2
    grPulse_ = (TGraph*)file->Get("grSignal_Phase2");
  }else if(iopt==3){ // Spike Phase 1
    grPulse_ = (TGraph*)file->Get("grSpike_Phase2");
  }
  xpeak_=0;
  ypeak_=0;
  double x,y;
  for (int i=0; i<grPulse_->GetN(); ++i){
    grPulse_->GetPoint(i,x,y);
    if (y>ypeak_) {
      ypeak_=y;
      xpeak_=x;
    }
  }
  file->Close();
}



Pulse::~Pulse()
{
  delete grPulse_;
}

