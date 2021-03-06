(TeX-add-style-hook
 "handoutShortcuts"
 (lambda ()
   (TeX-add-symbols
    '("pd" 2)
    "aAgg"
    "aboveMin"
    "adjPar"
    "adj"
    "aE"
    "aFunc"
    "Age"
    "age"
    "ALevBF"
    "aLevBF"
    "ALev"
    "aLev"
    "Alive"
    "Alt"
    "aMin"
    "ARat"
    "aRat"
    "ASS"
    "aSS"
    "ATarg"
    "aTarg"
    "BE"
    "bE"
    "BLevBF"
    "bLevBF"
    "BLevE"
    "bLevE"
    "BLevU"
    "bLevU"
    "BLev"
    "bLev"
    "bMin"
    "bRatE"
    "BRatE"
    "bRatU"
    "BRat"
    "bRat"
    "bTargE"
    "BTargTarg"
    "bTargTarg"
    "BTarg"
    "bTarg"
    "BU"
    "bU"
    "cAgg"
    "CARA"
    "ccRat"
    "CDF"
    "CEndFunc"
    "cEndFunc"
    "cEss"
    "CE"
    "cE"
    "cFuncAbove"
    "cFuncBelow"
    "cFuncMax"
    "CFunc"
    "cFunc"
    "CGroOverG"
    "CGroOverR"
    "CGroPF"
    "cGroPF"
    "CGroPS"
    "chiFunc"
    "Chi"
    "CLevBF"
    "cLevBF"
    "CLevE"
    "cLevE"
    "cLevFunc"
    "CLevU"
    "cLevU"
    "cLev"
    "CLev"
    "Cons"
    "cons"
    "corr"
    "cPDVFunc"
    "CPDV"
    "cPPP"
    "cPP"
    "cP"
    "cRatBF"
    "CRatE"
    "cRatE"
    "CRatU"
    "cRatU"
    "CRat"
    "cRat"
    "CRRA"
    "CTargE"
    "cTargE"
    "cTargTarg"
    "CTarg"
    "cTarg"
    "curr"
    "Curr"
    "CU"
    "cU"
    "dRat"
    "debtLim"
    "Debt"
    "debt"
    "DeprFac"
    "Depr"
    "depr"
    "deprRte"
    "DiscAltuAdj"
    "DiscAlt"
    "Discount"
    "DiscRate"
    "DiscRte"
    "DiscFac"
    "DivGro"
    "divGro"
    "Div"
    "div"
    "DLev"
    "Dvdnd"
    "dvdnd"
    "edvdnd"
    "EEndMap"
    "effUnits"
    "eFunc"
    "ELev"
    "ek"
    "EmpGro"
    "empGro"
    "empState"
    "EpremLog"
    "EPrem"
    "eprem"
    "EpShkInv"
    "erate"
    "error"
    "Err"
    "err"
    "Estdr"
    "Evarr"
    "EVarr"
    "expend"
    "Ex"
    "FDist"
    "fDist"
    "FFunc"
    "fFunc"
    "FLev"
    "fLev"
    "fPP"
    "FPP"
    "fP"
    "FP"
    "GLev"
    "GovNW"
    "govNW"
    "GovSpend"
    "govSpend"
    "Habit"
    "habit"
    "Ham"
    "HARKcore"
    "hEndMin"
    "hEnd"
    "hFunc"
    "Hi"
    "HLev"
    "HLevBF"
    "hLevBF"
    "hLev"
    "hMin"
    "HMin"
    "hours"
    "Hours"
    "HRat"
    "hRat"
    "h"
    "H"
    "iFunc"
    "IFunc"
    "ILev"
    "iLev"
    "impg"
    "ImpG"
    "impr"
    "ImpR"
    "Inc"
    "inc"
    "InvEpShkInv"
    "Inv"
    "inv"
    "IRat"
    "iRat"
    "itc"
    "jFunc"
    "JLev"
    "kapRent"
    "kapShare"
    "Kap"
    "kap"
    "KFunc"
    "kFunc"
    "KLevBF"
    "kLevBF"
    "KLev"
    "kLev"
    "kPriceAfterITC"
    "kPrice"
    "KRat"
    "kRat"
    "kTargE"
    "kTarg"
    "labor"
    "Labor"
    "labShare"
    "Leisure"
    "leisure"
    "leiShare"
    "LGro"
    "lGro"
    "LLevBF"
    "lLevBF"
    "lLev"
    "LLev"
    "Lo"
    "LRat"
    "MaxMaxMPC"
    "MaxMinMPC"
    "MaxMPC"
    "MaxMPS"
    "Mean"
    "mEss"
    "ME"
    "mE"
    "mFunc"
    "MinMinMPC"
    "MinMPC"
    "MinMPS"
    "MLevBF"
    "mLevBF"
    "mLevE"
    "MLev"
    "mLev"
    "MPCE"
    "MPCFunc"
    "MPCPPF"
    "MPCP"
    "MPCU"
    "MPC"
    "MPSFunc"
    "MPS"
    "MRatE"
    "mRatE"
    "MRat"
    "mRat"
    "MSS"
    "mSS"
    "mTarg"
    "MU"
    "mU"
    "Next"
    "nFunc"
    "NLev"
    "nLev"
    "NRat"
    "nRat"
    "Num"
    "nIter"
    "OLevBF"
    "oLevBF"
    "OLev"
    "oLev"
    "ORat"
    "oRat"
    "Pareto"
    "PatPGroAdj"
    "patpGroAdj"
    "patpGrohat"
    "PatPGro"
    "patpGro"
    "PatR"
    "patr"
    "PatU"
    "patu"
    "PatWGro"
    "patwGro"
    "Pat"
    "pat"
    "pDeadRate"
    "pDead"
    "pDieRate"
    "pDies"
    "PDies"
    "PDV"
    "PGroAdj"
    "pGroAdj"
    "PGrouAdj"
    "pGrouAdj"
    "PGro"
    "pGro"
    "phiFunc"
    "PIHMPC"
    "PInc"
    "PLabor"
    "Plabor"
    "PLevBF"
    "pLevBF"
    "PLev"
    "pLev"
    "PLives"
    "pLives"
    "pNotZero"
    "PopE"
    "popE"
    "PopGro"
    "popGro"
    "PopLev"
    "PopU"
    "Pop"
    "PostITC"
    "power"
    "pPDVFunc"
    "PPDV"
    "pRat"
    "Price"
    "ProdFunc"
    "prodFunc"
    "prudEx"
    "prud"
    "pSav"
    "pShkMin"
    "PShk"
    "PermShkAgg"
    "PermShk"
    "permShk"
    "pShk"
    "permShkInd"
    "pshk"
    "PtyGro"
    "ptyGro"
    "PtyLab"
    "ptyLab"
    "PtyLev"
    "ptyLev"
    "pZero"
    "QLev"
    "q"
    "RCpnd"
    "RevFunc"
    "revFunc"
    "Rev"
    "rev"
    "rfree"
    "Rfree"
    "RFunc"
    "RGross"
    "rGross"
    "RiskyAlt"
    "riskyAlt"
    "riskyshare"
    "Risky"
    "risky"
    "RLev"
    "RnormWGro"
    "rnormwGro"
    "Rnorm"
    "rnorm"
    "Rport"
    "rport"
    "Rprod"
    "rprod"
    "rProd"
    "RProd"
    "RSave"
    "rsave"
    "RBoro"
    "rboro"
    "saveRate"
    "Save"
    "save"
    "SDF"
    "sdr"
    "Seniority"
    "seniority"
    "SeverancePayment"
    "SeveranceRatio"
    "Severance"
    "SE"
    "sE"
    "sFunc"
    "shk"
    "Shk"
    "ShkLogZeroLogStd"
    "ShkLogZeroLogVar"
    "ShkLogZeroLog"
    "ShkLogZero"
    "ShkMeanOneLogStd"
    "ShkMeanOneLogVar"
    "ShkMeanOneLog"
    "ShkMeanOne"
    "SLevBF"
    "sLevBF"
    "SLevE"
    "sLevE"
    "SLevU"
    "sLevU"
    "SLev"
    "sLev"
    "srate"
    "SRatE"
    "sRatE"
    "SRatU"
    "sRatU"
    "SRat"
    "sRat"
    "STargE"
    "sTargE"
    "STargTarg"
    "sTargTarg"
    "STarg"
    "sTarg"
    "Steady"
    "Stocks"
    "stocks"
    "straight"
    "Surplus"
    "surplus"
    "SU"
    "sU"
    "Target"
    "TaxCombInv"
    "TaxComb"
    "TaxCorp"
    "taxDep"
    "TaxFree"
    "TaxLev"
    "TaxNetTrans"
    "taxNetTrans"
    "TaxPaid"
    "TaxRate"
    "TaxUI"
    "Tax"
    "tax"
    "tBak"
    "TEatBak"
    "TEat"
    "TEndBak"
    "TEnd"
    "TermTime"
    "tFwd"
    "tHorOfm"
    "tHor"
    "timeRate"
    "tinyAmount"
    "TLev"
    "TMap"
    "tNow"
    "tShkAll"
    "tShkEmpMin"
    "TShkEmp"
    "tShkEmp"
    "tranShkInd"
    "TranShkAgg"
    "TShk"
    "tShk"
    "tshk"
    "tSS"
    "tThen"
    "uFunc"
    "uInvEpShkuInv"
    "ULev"
    "uLev"
    "unins"
    "uPDVFunc"
    "uPmt"
    "uPPP"
    "uPP"
    "uP"
    "urate"
    "utilFunc"
    "util"
    "ValAlt"
    "valfn"
    "Value"
    "VEndFunc"
    "vEndFunc"
    "VEnd"
    "vEnd"
    "vEss"
    "VE"
    "vE"
    "vFirm"
    "VFunc"
    "vFunc"
    "VInv"
    "vInv"
    "vk"
    "vLevBF"
    "VLevFunc"
    "vLevFunc"
    "VLev"
    "vLev"
    "vNorm"
    "VNum"
    "vNum"
    "vOptAlt"
    "vOpt"
    "VRat"
    "vRat"
    "vTarg"
    "VU"
    "vU"
    "Wage"
    "wage"
    "WAllLev"
    "wAllLev"
    "WAllRat"
    "wAllRat"
    "WAll"
    "wAll"
    "WBeg"
    "wBeg"
    "Wealth"
    "wealth"
    "WEndRat"
    "wEndRat"
    "WEnd"
    "wEnd"
    "Wend"
    "wend"
    "wFunc"
    "WGroPF"
    "WGro"
    "wGro"
    "whumMin"
    "WHum"
    "wHum"
    "Whum"
    "whum"
    "WLev"
    "wLev"
    "WMid"
    "wMid"
    "Wmid"
    "wmid"
    "WMkt"
    "wMkt"
    "wmkt"
    "wNet"
    "WNet"
    "WPre"
    "wPre"
    "wRat"
    "WRat"
    "wTot"
    "WTot"
    "wtot"
    "Wtot"
    "xFer"
    "XFer"
    "xFunc"
    "XLev"
    "xLev"
    "xpend"
    "XperGro"
    "xperGro"
    "XRat"
    "xRat"
    "yFunc"
    "yLevBF"
    "YLev"
    "YLevBF"
    "yLev"
    "YRat"
    "yRat"
    "yTargE"
    "yTarg"
    "zAgg"
    "zFunc"
    "ZLevBF"
    "zLevBF"
    "ZLev"
    "zLev"
    "ZRat"
    "zRat"
    "discRte"
    "DieFac"
    "LivFac"
    "PopFac"
    "popRte"
    "NFALev"
    "NFARat"
    "NI"
    "GDPLev"
    "GDPRat"
    "GDPGro"
    "gdpLev"
    "gdpRat"
    "weight"
    "bi"
    "ei"
    "reqd"
    "recm"))
 :latex)

