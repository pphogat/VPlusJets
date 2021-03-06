from RooWjj2DFitterPars import Wjj2DFitterPars
from ROOT import kRed, kAzure, kGreen, kBlue, kCyan, kViolet, kGray, kYellow

def theConfig(Nj, mH, isElectron = False, initFile = [], includeSignal = True,
              btagged = False):
    pars = Wjj2DFitterPars()
    # pars.MCDirectory = '/uscms_data/d2/andersj/Wjj/2012/data/Moriond2013/ReducedTrees/'
    #pars.MCDirectory = '/uscms_data/d1/lnujj/RDTrees_BoostedW_2013_1_29/'
    pars.MCDirectory = 'root://cmseos:1094//eos/uscms/store/user/lnujj/BoostedDibosonFitPostMoriond2013/'
    pars.isElectron = isElectron
    #pars.btagSelection = btagged
    pars.boostedSelection = True
    pars.useTopSideband = False
    pars.extras = []
    pars.useTopMC = True
    pars.initialParametersFile = initFile

    ### Define the parameters of the fit to the data
    pars.backgrounds = ['diboson', 'top', 'WpJ']
    pars.includeSignal = includeSignal
    pars.signals = []
    #pars.constrainShapes = []
    #pars.yieldConstraints = {'top' : 0.07, 'WpJ' : 0.05 }
    #pars.constrainShapes = ['WpJ', 'top', 'diboson']
    pars.yieldConstraints = {'diboson' : 0.034, 'top' : 0.07}
    pars.constrainShapes = ['WpJ']

    #pars.yieldConstraints = {}

#    pars.yieldConstraints = {'top' : 0.50, 'WpJ' : 0.50 }
    #pars.constrainShapes = ['WpJ']

    pars.Njets = Nj
    pars.mHiggs = mH

    if isElectron:
        flavorString = 'el'
    else:
        flavorString = 'mu'


    pars.cuts = \
              '(W_pt>200.)&&(GroomedJet_CA8_pt[0]>200)' +\
              '&&(abs(GroomedJet_CA8_eta[0])<2.4)' +\
              '&&(GroomedJet_CA8_mass_pr[0]>40)' +\
              '&&(GroomedJet_CA8_tau2tau1[0]<0.55)'

    pars.btagVeto = False

    if pars.useTopSideband:
        pars.cuts += '&&(GroomedJet_numberbjets_csvm>=1)'
    # elif pars.btagSelection:
    #     pars.cuts += '&&(GroomedJet_numberbjets==1)'
    else:
        pars.cuts += '&&(ggdboostedWevt==1)' +\
                     '&&(GroomedJet_CA8_deltaphi_METca8jet>2.0)' +\
                     '&&(GroomedJet_CA8_deltaR_lca8jet>1.57)'
        pars.cuts += '&&(numPFCorJetBTags<1)'

        

    # veto vbf
    pars.cuts += '&&(vbf_event==0)'

    # you need a files entry and a models entry for each of the fit 
    # compoents in backgrounds and signals
    # the files should a list with entries like (filename, Ngen, xsec)
    
#################### Global Convolution Models ########################
    #pars.GlobalConvModels=[27]
    pars.GlobalConvModels=[-1]
    pars.GlobalConvModelsAlt=pars.GlobalConvModels
    
#####################  diboson: #######################################
    pars.dibosonFiles = [
        (pars.MCDirectory + 'RD_%s_WW_CMSSW532.root' % (flavorString),
         9450414, 57.1097),
        (pars.MCDirectory + 'RD_%s_WZ_CMSSW532.root' % (flavorString),
         10000267, 32.3161),
        ]

    pars.dibosonFracOfData = -1
    
##     if isElectron:
##         #pars.dibosonFracOfData = 0.733
##         pars.dibosonFracOfData = -1
##     else:
##         pars.dibosonFracOfData = 0.09048
##         #pars.dibosonFracOfData = -1

    #pars.dibosonModels = [5]
    pars.dibosonModels = [22]
    pars.dibosonModelsAlt = pars.dibosonModels
    pars.dibosonConvModels = pars.GlobalConvModels
    pars.dibosonConvModelsAlt = pars.dibosonConvModels
    

#####################  WpJ: ###########################################
    pars.WpJFiles = [
        (pars.MCDirectory + 'RD_%s_WJets_madgraph_CMSSW532.root' % (flavorString),
         8955318, 1.3*228.9),
        ]

    pars.WpJFracOfData = -1
    
##     if isElectron:
##         #pars.WpJFracOfData = 0.733
##         pars.WpJFracOfData = -1
##     else:
##         pars.WpJFracOfData = 0.6198
##         #pars.WpJFracOfData = -1

    pars.WpJModels = [3]
    #    pars.WpJModelsAlt = [8]
    #    pars.WpJModelsAlt = [308] ##Alt2 Model
    pars.WpJModelsAlt = [10] ##Alt3 Model
    pars.WpJAuxModelsAlt = [5]
    pars.WpJConvModels = pars.GlobalConvModels
    pars.WpJConvModelsAlt = pars.WpJConvModels

#####################  top: #######################################  
    ttkfactor = 0.95
    pars.topFiles = [
        (pars.MCDirectory + 'RD_%s_STopTW_Tbar_CMSSW532.root' % (flavorString),
         493458, 11.1773*ttkfactor),
        (pars.MCDirectory + 'RD_%s_STopTW_T_CMSSW532.root' % (flavorString),
         497657, 11.1773*ttkfactor),
        (pars.MCDirectory + 'RD_%s_TTJetsPoheg_CMSSW532.root' % (flavorString),
         20975917, 225.197*ttkfactor),
        (pars.MCDirectory + 'RD_%s_STopS_Tbar_CMSSW532.root' % (flavorString),
         139974, 1.75776*ttkfactor),
        (pars.MCDirectory + 'RD_%s_STopS_T_CMSSW532.root' % (flavorString),
         259960, 3.89394*ttkfactor),
        (pars.MCDirectory + 'RD_%s_STopT_Tbar_CMSSW532.root' % (flavorString),
         1935066, 30.0042*ttkfactor),
        (pars.MCDirectory + 'RD_%s_STopT_T_CMSSW532.root' % (flavorString),
         3758221, 55.531*ttkfactor),
        ]

    pars.topFracOfData = -1
    
##     if isElectron:
##         #pars.topFracOfData = 0.201
##         pars.topFracOfData = -1
##     else:
##         pars.topFracOfData = 0.2897
##         #pars.topFracOfData = -1


    #pars.topModels = [30]
    pars.topModels = [607]
    #    pars.topModelsAlt = pars.topModels
    pars.topModelsAlt = [330]
    #pars.topModelsAlt = [24]
    #pars.topAuxModelsAlt = [2]
    pars.topConvModels = pars.GlobalConvModels
    pars.topConvModelsAlt = pars.topConvModels

################################################################### 



    pars.dibosonPlotting = {'color' : kAzure+8, 'title' : 'WW+WZ'}
    pars.WpJPlotting = { 'color' : kRed, 'title' : 'V+jets'}
    pars.topPlotting = {'color' : kGreen+2, 'title' : 'top'}
    pars.ggHPlotting = {'color' : kBlue, 'title' : "ggH(%i) #rightarrow WW" % mH}

    pars.var = ['GroomedJet_CA8_mass_pr[0]']
    #pars.varRanges = {'GroomedJet_CA8_mass_pr[0]': (10, 40., 140., []),}
    pars.varRanges = {'GroomedJet_CA8_mass_pr[0]': (25, 70., 320., []),}
    pars.varTitles = {'GroomedJet_CA8_mass_pr[0]': 'm_{J}',
                      }
    pars.varNames = {'GroomedJet_CA8_mass_pr[0]': 'GroomedJet_CA8_mass_pr' }

    
    pars.exclude = {}
    pars.blind = False

    pars.integratedLumi = 19300.

    pars.binData = False
    # pars.binData = True

    return customizeElectrons(pars) if isElectron else \
        customizeMuons(pars)

def customizeElectrons(pars):
    pars.DataFile = pars.MCDirectory + 'RD_WenuJets_DataAllSingleElectronTrigger_GoldenJSON_19p2invfb.root'

    if pars.useTopSideband and not pars.useTopMC:
        pars.topFiles = [(pars.DataFile,1,1),]
    
    pars.integratedLumi = 19200.
    pars.doEffCorrections = True
    pars.effToDo = ['lepton']
    pars.leptonEffFiles = {
        'id': ["EffTable2012/scaleFactor-Run2012ABC-GsfElectronToId.txt"],
        'reco': ["EffTable2012/scaleFactor-Run2012ABC-SCToElectron.txt"],
        'HLT': ["EffTable2012/efficiency-Run2012ABC-WP80ToHLTEle.txt"]
        }
    pars.lumiPerEpoch = [pars.integratedLumi]

##     pars.cuts += '&&(W_electron_pt>30)'
    pars.cuts += '&&(event_met_pfmet >70)&&(W_electron_pt>35)'
    return pars

def customizeMuons(pars):
    pars.DataFile = pars.MCDirectory + 'RD_WmunuJets_DataAll_GoldenJSON_19p3invfb.root'

    if pars.useTopSideband and not pars.useTopMC:
        pars.topFiles = [(pars.DataFile,1,1),]
    
    pars.doEffCorrections = True
    pars.effToDo = ['lepton']
    pars.leptonEffFiles = {
        'id': ["EffTable2012/scaleFactor-Run2012ABC-RecoToIso.txt"],
        'HLT': ["EffTable2012/efficiency-Run2012ABC-IsoToIsoMuHLT.txt"]
        }
    pars.lumiPerEpoch = [pars.integratedLumi]

    pars.cuts += '&&(event_met_pfmet >50)&&(abs(W_muon_eta)<2.1)&&(W_muon_pt>30.)'
    
    return pars
