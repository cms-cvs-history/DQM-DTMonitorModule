import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")
process.load("Geometry.DTGeometry.dtGeometry_cfi")

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cff")

process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi")

process.load("RecoMuon.DetLayers.muonDetLayerGeometry_cfi")

process.load("DQMServices.Core.DQM_cfg")

process.source = cms.Source("EmptyIOVSource",
    lastRun = cms.untracked.uint32(100),
    timetype = cms.string('runnumber'),
    firstRun = cms.untracked.uint32(1),
    interval = cms.uint32(90)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.eventInfoProvider = cms.EDFilter("EventCoordinatesSource",
    eventInfoFolder = cms.untracked.string('EventInfo/')
)

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('resolutionTest_step1', 
        'resolutionTest_step2', 
        'resolutionTest_step3'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('ERROR'),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        resolution = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        noLineBreaks = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('resolution'),
    destinations = cms.untracked.vstring('cout')
)

process.qTester = cms.EDFilter("QualityTester",
    prescaleFactor = cms.untracked.int32(1),
    qtList = cms.untracked.FileInPath('DQM/DTMonitorClient/test/QualityTests_ttrig.xml')
)

process.resolutionTest_step1 = cms.EDFilter("DTResolutionTest",
    OutputMEsInRootFile = cms.bool(False),
    runningStandalone = cms.untracked.bool(True),
    resDistributionTestName = cms.untracked.string('ResidualsDistributionGaussianTest'),
    histoTag2D = cms.untracked.string('hResDistVsDist_STEP1'),
    calibModule = cms.untracked.bool(True),
    meanTestName = cms.untracked.string('ResidualsMeanInRange'),
    STEP = cms.untracked.string('STEP1'),
    folderRoot = cms.untracked.string(''),
    sigmaTestName = cms.untracked.string('ResidualsSigmaInRange'),
    debug = cms.untracked.bool(False),
    diagnosticPrescale = cms.untracked.int32(1),
    histoTag = cms.untracked.string('hResDist_STEP1'),
    inputFile = cms.untracked.string('/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/DTkFactValidation_RUNNUMBERTEMPLATE.root')
)

process.resolutionTest_step2 = cms.EDFilter("DTResolutionTest",
    OutputMEsInRootFile = cms.bool(False),
    runningStandalone = cms.untracked.bool(True),
    resDistributionTestName = cms.untracked.string('ResidualsDistributionGaussianTest'),
    histoTag2D = cms.untracked.string('hResDistVsDist_STEP2'),
    calibModule = cms.untracked.bool(True),
    meanTestName = cms.untracked.string('ResidualsMeanInRange'),
    STEP = cms.untracked.string('STEP2'),
    folderRoot = cms.untracked.string(''),
    sigmaTestName = cms.untracked.string('ResidualsSigmaInRange'),
    debug = cms.untracked.bool(False),
    diagnosticPrescale = cms.untracked.int32(1),
    histoTag = cms.untracked.string('hResDist_STEP2'),
    inputFile = cms.untracked.string('/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/DTkFactValidation_RUNNUMBERTEMPLATE.root')
)

process.resolutionTest_step3 = cms.EDFilter("DTResolutionTest",
    OutputMEsInRootFile = cms.bool(True),
    runningStandalone = cms.untracked.bool(True),
    resDistributionTestName = cms.untracked.string('ResidualsDistributionGaussianTest'),
    histoTag2D = cms.untracked.string('hResDistVsDist_STEP3'),
    calibModule = cms.untracked.bool(True),
    OutputFileName = cms.string('/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/SummaryResiduals_RUNNUMBERTEMPLATE.root'),
    meanTestName = cms.untracked.string('ResidualsMeanInRange'),
    STEP = cms.untracked.string('STEP3'),
    folderRoot = cms.untracked.string(''),
    sigmaTestName = cms.untracked.string('ResidualsSigmaInRange'),
    debug = cms.untracked.bool(False),
    diagnosticPrescale = cms.untracked.int32(1),
    histoTag = cms.untracked.string('hResDist_STEP3'),
    inputFile = cms.untracked.string('/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/DTkFactValidation_RUNNUMBERTEMPLATE.root')
)

process.secondStep = cms.Sequence(process.resolutionTest_step1*process.resolutionTest_step2*process.resolutionTest_step3*process.qTester)
process.p = cms.Path(process.secondStep)
process.DQM.collectorHost = ''


