#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 13:17:10 2017

@author: khiri
"""


class Zone(object):
    '''
    Classe Zone
    ---------------
    
    
    '''

    def __init__(self, identifier ="Z0", cTime=0, Khv = 1, K = 0, latencyV = 9, presences = []):
        '''
        Constructor
        '''
        self.identifier = identifier
        self.K = {cTime : K}
        self.Cvh = {cTime : 1}
        self.Chv = {cTime : 1}
        self.cTime = cTime
        self.presences = {cTime : presences}
        
        self.lambdaHV = {cTime : 0.}
        self.lambdaVH = {cTime : 0.}
        
        self.deltaVH = []
        self.deltaHV = []
        
        
        ### Moustiques
        self.Nv = {cTime : 100}
        self.latencyV = latencyV
        self.Sv = {cTime : self.Nv[cTime]}
        self.Ev = {cTime : 0}
        self.Iv = {cTime : 0}
        
        # constantes par défaut valeurs pour endémicité minimale
        self.betaVH = 0.01
        self.betaHV = 0.072
        self.betaHVt = 0.0072
        self.sigmaV = 0.1
        self.sigmaH = 0.1
        
        self.mu1V = 0.033
        self.mu2V = 4E-5
        self.psiV = 0.13
        
        ### Humains present dans la zone selon etat
        self.Nhc = {cTime : 0}
        self.Shc = {cTime : 0}
        self.Ehc = {cTime : 0}
        self.Ihc = {cTime : 0}
        self.Rhc = {cTime : 0}
        ## I et R pris en compte dans le calcul de FOI
        self.Ihnp = {cTime : 0}
        self.Rhnp = {cTime : 0}
        
        #humain résident dans la zone selon etat
        self.Nhr = {cTime : 0}
        self.Shr = {cTime : 0}
        self.Ehr = {cTime : 0}
        self.Ihr = {cTime : 0}
        self.Rhr = {cTime : 0}
        #nb de nouveaux exposés résidents dans la zone
        self.Eh0 = {cTime : 0}
    
        
        ### proportion relative aux proba (espérances)
        self.Es = {cTime : 0}
        self.Ee = {cTime : 0}
        self.Ei = {cTime : 0}
        self.Er = {cTime : 0}
        
        self.E0 = {cTime : 0}
        self.listePse = {cTime : []}
        
        
    def getId(self):
        return self.identifier
        
    def getTime(self):
        return self.cTime
        
    def getK(self, time):
        return self.K[time]
    
    def getSv(self, time):
        return self.Sv[time]
        
    def getEv(self, time):
        return self.Ev[time]
        
    def getIv(self, time):
        return self.Iv[time]
        
    def getLambdaHV(self, time):
        return self.lambdaHV[time]
        
    def getLambdaVH(self, time):
        return self.lambdaVH[time]
    
    def getPresences(self, time):
        return self.presences[time]
    
    def setId(self, i):
        self.identifier = "Z" + str(i)
        
    def setTime(self, time):
        self.cTime = time
        
    def setK(self, K, time):
        self.K[time] = K
    
    def setNv(self, Nv, time):
        self.Nv[time] = Nv
        
    def setSv(self, Sv, time):
        self.Sv[time] = Sv
        
    def setEv(self, Ev, time):
        self.Ev[time] = Ev
        
    def setIv(self, Iv, time):
        self.Iv[time] = Iv
       
    def setLambdaHV(self, lambdaHV, time):
        self.lambdaHV[time] = lambdaHV
        
    def setLambdaVH(self, lambdaVH, time):
        self.lambdaVH[time] = lambdaVH
        
    def setPresence(self, presences, time):
        self.presences[time] = presences
        
    def addPresence(self, presence, time):
        self.presences[time].append(presence)
        
    def setParameters(self, K):
        # constantes
        betaVHmin = 0.01
        betaVHmax = 0.27
        betaHVmin = 0.072
        betaHVmax = 0.64
        betaHVtmin = 0.0072
        betaHVtmax = 0.064
        sigmaVmin = 0.1
        sigmaVmax = 1.0
        sigmaHmin = 0.1
        sigmaHmax = 50
        
        #valeurs retenues par chitnis et al (population moustiques positive stable)
        mu1Vmin = 0.033
        mu1Vmax = 0.033
        mu2Vmin = 2E-5
        mu2Vmax = 4E-5
        psiVmin = 0.13
        psiVmax = 0.13
        
        self.betaVH = betaVHmin + K * (betaVHmax - betaVHmin)
        self.betaHV = betaHVmin + K * (betaHVmax - betaHVmin)
        self.betaHVt = betaHVtmin + K * (betaHVtmax - betaHVtmin)
        self.sigmaV = sigmaVmin + K * (sigmaVmax - sigmaVmin)
        self.sigmaH = sigmaHmin + K * (sigmaHmax - sigmaHmin)
        
        self.mu1V = mu1Vmax - K * (mu1Vmax - mu1Vmin)
        self.mu2V = mu2Vmax - K * (mu2Vmax - mu2Vmin)
        self.psiV = psiVmin + K * (psiVmax - psiVmin)
        
    
    def __str__(self):
        string =""
        string = string +"Identifiant : "+ str(self.identifier)+"\n"
        string = string + "K : "+str(self.K)+"\n"
        string = string + "LambdaHV : "+str(self.lambdaHV[self.cTime])+"\n"
        string = string + "LambdaVH : "+str(self.lambdaVH[self.cTime])+"\n"
        string = string + "Presences :"+str(self.presences[self.cTime])
        return string