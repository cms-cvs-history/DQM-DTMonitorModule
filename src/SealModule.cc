#include "PluginManager/ModuleDef.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include <DQM/DTMonitorModule/interface/DTDigiTask.h>
DEFINE_FWK_MODULE(DTDigiTask);

#include <DQM/DTMonitorModule/interface/DTTestPulsesTask.h>
DEFINE_ANOTHER_FWK_MODULE(DTTestPulsesTask);

#include "DQM/DTMonitorModule/interface/DTLocalRecoTask.h"
DEFINE_ANOTHER_FWK_MODULE(DTLocalRecoTask);

#include "DQM/DTMonitorModule/interface/DTTriggerCheck.h"
DEFINE_ANOTHER_FWK_MODULE(DTTriggerCheck);

#include <DQM/DTMonitorModule/interface/DTDataIntegrityTask.h>
#include "FWCore/ServiceRegistry/interface/ServiceMaker.h"

using namespace edm::serviceregistry;

//typedef ParameterSetMaker<DTDataMonitorInterface,DTDataIntegrityTask> maker;
typedef edm::serviceregistry::AllArgsMaker<DTDataMonitorInterface,DTDataIntegrityTask> maker;

DEFINE_ANOTHER_FWK_SERVICE_MAKER(DTDataIntegrityTask,maker);
