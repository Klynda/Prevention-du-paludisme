#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 17:41:10 2017

@author: khiri
"""
from Etat import Etat
from Zone import Zone
import random

class Individu(object):
    '''
    Classe Individu
    ---------------
    Par defaut un individu est initialisé à l'état sain avec Ps=1 les autres
    probabilités Pe = Pi = Pr = 0
    Les déplacement ne sont pas connus
    '''


    def __init__(self, identifier ="H0", cTime = 0, state = Etat('S', 0), Ps=1, Pe=0, Pi=0, Pr=0, path=[], g = None):
        '''
        Constructor
        '''
        self.identifier = identifier
        self.cTime = cTime
        self.state = {cTime : state}
        self.Ps = {cTime : Ps}
        self.Pse = {cTime : 0}
        self.Pe = {cTime : Pe}
        self.Pei = {cTime : 0}
        self.Pi = {cTime : Pi}
        self.Pir = {cTime : 0}
        self.Pr = {cTime : Pr}
        self.Prs = {cTime : 0}
        self.lambdaVH = {cTime : 0}
        self.path = {cTime : path}
        
        ### constantes
        self.latencyH=10 #entre 9 et 10 à voir
        self.infectiousH= 9.5*30     #chitnis 9.5*30
        self.imuneH=5*365
        if g == None :
            g = random.Random()
        
        self.threshold = g.uniform(0., 1)
        
        ### valeur entre 0 et 1 :individu non protogé par defaut 0
        self.protected = {cTime : 0}

    def getIdentifier(self):
        return self.identifier
        
    def getLatencyH(self):
        return self.latencyH
        
    def getInfectiousH(self):
        return self.infectiousH
        
    def getImuneH(self):
        return self.imuneH
        
    def getId(self):
        return self.identifier
    
    def getTime(self):
        return self.cTime
        
    def getState(self, time):
        return self.state[time]
       
    def getPs(self, time):
        return self.Ps[time]
    
    def getPse(self, time):
        return self.Pse[time]
        
    def getPe(self, time):
        return self.Pe[time]
    
    def getPei(self, time):
        return self.Pei[time]
    
    def getPi(self, time):
        return self.Pi[time]
    
    def getPir(self, time):
        return self.Pir[time]
    
    def getPr(self, time):
        return self.Pr[time]
    
    def getPrs(self, time):
        return self.Prs[time]
    
    def getLambdaVH(self, time):
        return self.lambdaVH[time]
    
    def getPath(self, time):
        return self.path[time]
    
    def getProtected(self, time):
        return self.protected[time]
    
    def setId(self, i):
        self.identifier = "H" + str(i)
    
    def setTime(self, time):
        self.cTime = time
        
    def setState(self, state, time):
        self.state[time] = state
       
    def setPs(self, Ps, time):
        self.Ps[time] = Ps
        
    def setPse(self, Pse, time):
        self.Pse[time] = Pse
        
    def setPe(self, Pe, time):
        self.Pe[time] = Pe
    
    def setPei(self, Pei, time):
        self.Pei[time] = Pei
    
    def setPi(self, Pi, time):
        self.Pi[time] = Pi
        
    def setPir(self, Pir, time):
        self.Pir[time] = Pir
    
    def setPr(self, Pr, time):
        self.Pr[time] = Pr
        
    def setPrs(self, Prs, time):
        self.Prs[time] = Prs   
        
    def setLambdaVH(self, lambdaVH, time):
        self.lambdaVH[time] = lambdaVH
    
        
    def setPath(self, path, time):
        self.path[time] = path
        
    def setProtected(self, protected, time):
        self.protected[time] = protected           

    
    def __str__(self):
        string =""
        string = string +"Identifiant : "+ str(self.identifier)+"\n"
        string = string + "Etat : "+str(self.state[self.cTime])+"\nProbas : ("
        string = string + str(self.Ps[self.cTime])+" ; "+str(self.Pe[self.cTime])+" ; "+str(self.Pi[self.cTime])+" ; "+str(self.Pr[self.cTime])+")\n"
        string = string + "Trajet :"+str(self.path[self.cTime])
        return string
        

    