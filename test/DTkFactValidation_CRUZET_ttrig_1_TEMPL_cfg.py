import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")
process.load("Geometry.DTGeometry.dtGeometry_cfi")
process.DTGeometryESModule.applyAlignment = False

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cff")

process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi")

process.load("RecoMuon.DetLayers.muonDetLayerGeometry_cfi")

process.load("DQMServices.Core.DQM_cfg")

# The module for 1D DT RecHit building
process.load("RecoLocalMuon.DTRecHit.dt1DRecHits_LinearDrift_CosmicData_cfi")

# _Vdrift2D_ ##
process.load("RecoLocalMuon.DTSegment.dt2DSegments_CombPatternReco2D_LinearDrift_CosmicData_cfi")

# _4DAlgo ##
process.load("RecoLocalMuon.DTSegment.dt4DSegments_CombPatternReco4D_LinearDrift_CosmicData_cfi")

from CalibTracker.Configuration.Common.PoolDBESSource_cfi import poolDBESSource
poolDBESSource.connect = "frontier://FrontierDev/CMS_COND_ALIGNMENT"
poolDBESSource.toGet = cms.VPSet(cms.PSet(
        record = cms.string('GlobalPositionRcd'),
        tag = cms.string('IdealGeometry')
    )) 
process.glbPositionSource = poolDBESSource

process.source = cms.Source("PoolSource",
    debugFlag = cms.untracked.bool(True),
    debugVebosity = cms.untracked.uint32(10),
    fileNames = cms.untracked.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.dtunpacker = cms.EDFilter("DTUnpackingModule",
    dataType = cms.string('DDU'),
    useStandardFEDid = cms.untracked.bool(True),
    fedbyType = cms.untracked.bool(True),
    readOutParameters = cms.PSet(
        debug = cms.untracked.bool(False),
        rosParameters = cms.PSet(
            writeSC = cms.untracked.bool(True),
            readingDDU = cms.untracked.bool(True),
            performDataIntegrityMonitor = cms.untracked.bool(False),
            readDDUIDfromDDU = cms.untracked.bool(True),
            debug = cms.untracked.bool(False),
            localDAQ = cms.untracked.bool(False)
        ),
        localDAQ = cms.untracked.bool(False),
        performDataIntegrityMonitor = cms.untracked.bool(False)
    )
)

process.DTMapping = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('DTReadOutMappingRcd'),
        tag = cms.string('map_CRUZET')
    ), 
        cms.PSet(
            record = cms.string('DTT0Rcd'),
            tag = cms.string('TZEROTEMPLATE')
        ), 
        cms.PSet(
            record = cms.string('DTStatusFlagRcd'),
            tag = cms.string('NOISETEMPLATE')
        )),
    connect = cms.string('frontier://FrontierProd/CMS_COND_20X_DT'),      
    #connect = cms.string('oracle://cms_orcoff_prod/CMS_COND_20X_DT'),
    #        string connect = "frontier://Frontier/CMS_COND_ON_20X_DT"
    siteLocalConfig = cms.untracked.bool(False)
)

process.TTrig = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('ttrig')
    )),
    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/ttrig_second_RUNNUMBERTEMPLATE.db'),
    authenticationMethod = cms.untracked.uint32(0)
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

process.DTkFactValidation = cms.EDFilter("DTCalibValidation",
    # Write the histos on file
    OutputMEsInRootFile = cms.bool(True),
    # Lable to retrieve 2D segments from the event
    segment2DLabel = cms.untracked.string('dt2DSegments'),
    OutputFileName = cms.string('residuals.root'),
    # Lable to retrieve 4D segments from the event
    segment4DLabel = cms.untracked.string('dt4DSegments'),
    debug = cms.untracked.bool(False),
    # Lable to retrieve RecHits from the event
    recHits1DLabel = cms.untracked.string('dt1DRecHits')
)

process.qTester = cms.EDFilter("QualityTester",
    prescaleFactor = cms.untracked.int32(1),
    qtList = cms.untracked.FileInPath('DQM/DTMonitorClient/test/QualityTests.xml')
)

process.resolutionTest_step1 = cms.EDFilter("DTResolutionTest",
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
    inputFile = cms.untracked.string('residuals.root')
)

process.resolutionTest_step2 = cms.EDFilter("DTResolutionTest",
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
    inputFile = cms.untracked.string('residuals.root')
)

process.resolutionTest_step3 = cms.EDFilter("DTResolutionTest",
    runningStandalone = cms.untracked.bool(True),
    resDistributionTestName = cms.untracked.string('ResidualsDistributionGaussianTest'),
    histoTag2D = cms.untracked.string('hResDistVsDist_STEP3'),
    calibModule = cms.untracked.bool(True),
    meanTestName = cms.untracked.string('ResidualsMeanInRange'),
    STEP = cms.untracked.string('STEP3'),
    folderRoot = cms.untracked.string(''),
    sigmaTestName = cms.untracked.string('ResidualsSigmaInRange'),
    debug = cms.untracked.bool(False),
    diagnosticPrescale = cms.untracked.int32(1),
    histoTag = cms.untracked.string('hResDist_STEP3'),
    inputFile = cms.untracked.string('residuals.root')
)

process.firstStep = cms.Sequence(process.dtunpacker*process.dt1DRecHits*process.dt2DSegments*process.dt4DSegments*process.DTkFactValidation)
process.secondStep = cms.Sequence(process.resolutionTest_step1*process.resolutionTest_step2*process.resolutionTest_step3*process.qTester)
process.p = cms.Path(process.firstStep)
process.DQM.collectorHost = ''
process.DTLinearDriftAlgo_CosmicData.recAlgoConfig.hitResolution = 0.05
process.DTLinearDriftAlgo_CosmicData.recAlgoConfig.tTrigModeConfig.kFactor = -1.00
process.DTCombinatorialPatternReco2DAlgo_LinearDrift_CosmicData.Reco2DAlgoConfig.segmCleanerMode = 2
process.DTCombinatorialPatternReco2DAlgo_LinearDrift_CosmicData.Reco2DAlgoConfig.MaxAllowedHits = 30
process.DTCombinatorialPatternReco4DAlgo_LinearDrift_CosmicData.Reco4DAlgoConfig.segmCleanerMode = 2


