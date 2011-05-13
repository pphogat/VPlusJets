import FWCore.ParameterSet.Config as cms
isMC = False

process = cms.Process("demo")

##---------  Load standard Reco modules ------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')



##----- this config frament brings you the generator information ----
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("Configuration.StandardSequences.Generator_cff")


##----- Detector geometry : some of these needed for b-tag -------
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi")
process.load("RecoMuon.DetLayers.muonDetLayerGeometry_cfi")


##----- B-tags --------------
process.load("RecoBTag.Configuration.RecoBTag_cff")


##----- Global tag: conditions database ------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')



############################################
if not isMC:
    process.GlobalTag.globaltag = 'GR_R_311_V2::All'
else:
    process.GlobalTag.globaltag = 'START311_V2A::All'

OutputFileName = "demo.root"
numEventsToRun = -1
############################################

############################################
########################################################################################
########################################################################################
## Temporary conditions database for 2011 data until JEC goes into global tag
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.jec = cms.ESSource("PoolDBESSource",
      DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0)
        ),
      timetype = cms.string('runnumber'),
      toGet = cms.VPSet(
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Jec11V0_AK5PF'),
            label  = cms.untracked.string('AK5PF')
            )
      ),
## here you add as many jet types as you need (AK5Calo, AK5JPT, AK7PF, AK7Calo, KT4PF, KT4Calo)
      connect = cms.string('frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS')
)
process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')
########################################################################################
########################################################################################

##---------  Z-->ee Collection ------------
process.load("ElectroWeakAnalysis.VPlusJets.ZeeCollections_cfi")

##---------  Jet Collection ----------------
process.load("ElectroWeakAnalysis.VPlusJets.JetCollections_cfi")

##---------  Vertex and track Collections -----------
process.load("ElectroWeakAnalysis.VPlusJets.TrackCollections_cfi")
#


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numEventsToRun)
)

process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000



process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(
       '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/312/90646AF9-F957-E011-B0DB-003048F118C4.root',
       '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/312/749B54BD-E557-E011-AC27-000423D33970.root',
       '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/312/5A366F5F-7959-E011-AB12-0030487C8E02.root',
       '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/312/0EF76BBA-0858-E011-AE3A-003048F118C6.root',
       '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/312/024D65F9-F957-E011-8C5D-003048F024FE.root',

##        '/store/mc/Fall10/ZJetToEE_Pt_120to170_TuneZ2_7TeV_pythia6/GEN-SIM-RECO/START38_V12-v1/0001/E82FBD2C-21C9-DF11-B7FB-0022649E7902.root',
) )



##-------- Electron events of interest --------
process.HLTEle =cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
     HLTPaths = cms.vstring("HLT_Ele27_*", "HLT_Ele22_*", "HLT_Ele18_*", "HLT_Ele17_*", "HLT_Ele15_*"),
     eventSetupPathsKey = cms.string(''),
     andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
     throw = cms.bool(False) # throw exception on unknown path names
 )



process.VpusJets = cms.EDAnalyzer("VplusJetsAnalysis",
    srcPFCor = cms.InputTag("ak5PFJetsCorClean"),
    srcVectorBoson = cms.InputTag("bestZee"),
    VBosonType     = cms.string('Z'),
    LeptonType     = cms.string('electron'),                          
    runningOverMC = cms.untracked.bool(isMC),                                  
    srcGen  = cms.InputTag("ak5GenJets"),
    srcFlavorByValue = cms.InputTag("ak5tagJet"),
    srcPrimaryVertex = cms.InputTag("primaryVertex"),                                    
    HistOutFile = cms.string( OutputFileName ),
    TreeName    = cms.string('ZJet')                          
)




process.myseq = cms.Sequence(
    process.TrackVtxPath *     
    process.HLTEle *
    process.ZPath *    
    process.GenJetPath *
    process.impactParameterTagInfos * 
    process.secondaryVertexTagInfos *
    process.TagJetPath *
    process.PFJetPath *
    process.CorPFJetPath 
    )


if isMC:
    process.myseq.remove ( process.noscraping)
    process.myseq.remove ( process.HLTEle)
else:
    process.myseq.remove ( process.genParticles)
    process.myseq.remove ( process.GenJetPath)
    process.myseq.remove ( process.TagJetPath)


##---- if do not want to require >= 2 jets then disable that filter ---
process.myseq.remove ( process.RequireTwoJets)  


process.p = cms.Path( process.myseq * process.VpusJets)
