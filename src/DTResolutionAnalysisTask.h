#ifndef DTResolutionAnalysisTask_H
#define DTResolutionAnalysisTask_H

/** \class DTResolutionAnalysis
 *  DQM Analysis of 4D DT segments, it produces plots about: <br>
 *      - number of segments per event <br>
 *      - position of the segments in chamber RF <br>
 *      - direction of the segments (theta and phi projections) <br>
 *      - reduced chi-square <br>
 *  All histos are produce per Chamber
 *
 *
 *  $Date: 2006/10/08 16:03:21 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <FWCore/Framework/interface/EDAnalyzer.h>

#include <string>
#include <map>
#include <vector>

class DaqMonitorBEInterface;
class MonitorElement;


class DTResolutionAnalysisTask: public edm::EDAnalyzer{
public:
  /// Constructor
  DTResolutionAnalysisTask(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~DTResolutionAnalysisTask();

  /// BeginJob
  void beginJob(const edm::EventSetup& c);

  /// Endjob
  void endJob();

  // Operations
  void analyze(const edm::Event& event, const edm::EventSetup& setup);

protected:

private:
  DaqMonitorBEInterface* theDbe;

  // Switch for verbosity
  bool debug;
  std::string theRootFileName;
  bool writeHisto;

  // Lable of 4D segments in the event
  std::string theRecHits4DLabel;
  // Lable of 1D rechits in the event
  std::string theRecHitLabel;
  
  edm::ParameterSet parameters;

  // Book a set of histograms for a give chamber
  void bookHistos(DTSuperLayerId slId);
  // Fill a set of histograms for a give chamber 
  void fillHistos(DTSuperLayerId slId,
		  float distExtr,
		  float residual);
  
  std::map<DTSuperLayerId, std::vector<MonitorElement*> > histosPerSL;
};
#endif
