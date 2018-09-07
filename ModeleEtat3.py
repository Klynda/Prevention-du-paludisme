#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 13:28:00 2017

@author: khiri
"""
import random
import numpy as np
from Individu import Individu
from Etat import Etat
from Zone import Zone


class Modele(object):
    '''
    classe Modele
    -----------
    Modelise les déplacements des individus et mise à jour des zones
    
    
    '''


    def __init__(self, N , M, g=None):
        '''
        Constructor :
            cTime : temps courant (initialisé à 0)
            N : nombre de zones
            M : nombre d'individus
            zones : dictionnaire de zones de la forme : {"id" : Zone }
            humans : dictionnaire d'individu de la forme :{"id" : Individu }
                   
        '''
        self.cTime = 0  #temps courant
        self.N = N
        self.M = M
        
        #Création des zones
        self.zones = dict()
        for i in range(1, self.N+1, 1):
            zoneId = "Z"+str(i)
            self.zones[zoneId] = Zone(identifier = zoneId)
            
        #generateur aleatoire pour les individus
        self.g = g
        
        #Création des humains   
        self.humans = dict()  
        for j in range(1, self.M+1, 1):
            humanId = "H"+str(j)
            self.humans[humanId] = Individu(identifier=humanId, g = self.g)
            
        #listI contient la liste des nouveaux infectieux connus au temps courant
        self.listI = {}
        #lieu de résidence pour chaque individu
        self.residences = {}
        
        
        #temps de demoustication (par défaut non)
        self.tDem = np.inf
        #proportion de demoustication (par défaut non)
        self.pDem = 0
        #zone à démoustiquer
        self.idDem = ''
        
        self.event = False #presence d'un événement par defaut NON
        self.eventTime = np.inf
        #liste des individus nouvellement exposés pour chaque pas de temps
        self.listE0 = {0:[]}
        self.g = random.Random()
        self.g.seed()
        
        
    def getNbZones(self):
        return self.N
    
    def getNbHumans(self):
        return self.M
    
    def getHumans(self) :
        return self.humans

    def getZones(self):
        return self.zones
        
    def setCurrentTime(self, time):
        #permet de travailler sur le temps courant 'time'
        self.cTime = time
        for idz in self.zones.keys():
            print idz
            print time
            self.zones[idz].setTime(time)
        for idh in self.humans.keys():
            self.humans[idh].setTime(time)
            
    
    def initTravels(self, paths, presences):
        '''
        reçoit les déplacements et presences prédéfinis
        
        SUPPOSE QU'ILS CORRESPONDENT AU BON NOMBRE D'INDIVIDUS ET ZONES
        '''
        #self.cTime=0
        for idH , path in paths.iteritems():
            self.humans[idH].setPath(path, self.cTime)
            
        for idZ , presence in presences.iteritems():
            self.zones[idZ].setPresence(presence, self.cTime)
        
    
    def initStatesAndProba(self, infectedProp=None, recoverProp = None) :
        '''
        Introduit une proportion d'individus infectés ou rétablis et initialise les probabilités
        en fonction de cette proportion
        
        Les individus infectés sont choisis aléatoirement sans distinguer les 
        fixes des mobiles
        
        Si aucune proportion n'est précisée, cela veut dire que pas d'individu infecté
        ou rétabli
        
        Retourne : le couple (listI, listR)
        '''
        listI = []
        listR = []
        
        self.cTime=0
        g = random.Random()
        g.seed()
        
        listIndice = list(np.arange(1, self.M+1))
        #print listIndice
        
        if infectedProp != None :
            nbI = int(self.M* infectedProp)
            for i in range(nbI):
                j = g.randint(0, len(listIndice)-1)
                #print "liste :"+str(listIndice)
                #print "indice retenu :"+str(j)
                k = listIndice.pop(j)
                #print "id choisi : "+str(k)
                humanId = "H"+str(k)
                self.humans[humanId].setState(Etat('I', 0), self.cTime) #mettre etat à I(0)
                self.humans[humanId].setPse(0, self.cTime)
                listI.append(humanId)
        #print "liste infectés définitives :"+str(listI)
        
        if recoverProp != None :
            nbR = int(self.M* recoverProp)
            for i in range(nbR):
                j = g.randint(0, len(listIndice)-1)
                k = listIndice.pop(j)
                humanId = "H"+str(k)
                self.humans[humanId].setState(Etat('R', 0), self.cTime) #mettre etat à I(0)
                self.humans[humanId].setPse(0, self.cTime)
                listR.append(humanId)
        
        ir = (listI, listR)
        #mise à jour des zones
        for i in range(1, self.N+1, 1):
            
            zoneId = "Z"+str(i)
            zone = self.zones[zoneId]
            presences = zone.getPresences(self.cTime)
            
            
            ##########################
            #MISE A JOUR DES EFFECTIFS
            
            for humanId, duration in presences :
                human = self.humans[humanId]
                label = human.getState(self.cTime).getLabel()
                protected = human.getProtected(self.cTime)
                if label == 'I' :
                    zone.Ihc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    zone.Ihnp[self.cTime] += (1-protected)*duration
                if label == 'R' :
                    zone.Rhc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    zone.Rhnp[self.cTime] += (1-protected)*duration
                if label == 'S' :
                    zone.Shc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                if label == 'E' :
                    zone.Ehc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    
        return ir #Retourne : le couple (listI, listR)
    
    def initStatesAndProba2(self, listI=None, listR=None) :
        '''
        SUPPOSE QUE LES INDIVIDUS AIENT DÉJÀ ÉTÉ INITIALISÉS avec initTravels
        Introduit une proportion d'individus infectés et initialise les probabilités
        en fonction de cette proportion
        
        Les individus infectés sont choisis aléatoirement sans distinguer les 
        fixes des mobiles
        
        À AMÉLIORER CAR NE RENVOIE QUE LES Individus INFECTÉS ON PEUT RAJOUTER L'OPTION DE RETOURNER
        LES INDIVIDUS RÉTABLI -> NE PAS OUBLIER D'ADAPTER LE MAIN 
        
        '''
        
        self.cTime=0
        g = random.Random()
        g.seed()
        
        if listI != None :
            for humanId in listI :
                self.humans[humanId].setState(Etat('I', 0), self.cTime) #mettre etat à I(0)
        
        if listR != None :
            for humanId in listR :
                self.humans[humanId].setState(Etat('R', 0), self.cTime) #mettre etat à R(0)
                      
        
        #mise à jour des zones
        for i in range(1, self.N+1, 1):
            
            zoneId = "Z"+str(i)
            zone = self.zones[zoneId]
            presences = zone.getPresences(self.cTime)
            
            
            ##########################
            #MISE A JOUR DES EFFECTIFS
            
            for humanId, duration in presences :
                human = self.humans[humanId]
                label = human.getState(self.cTime).getLabel()
                protected = human.getProtected(self.cTime)
                
                if label == 'I' :
                    zone.Ihc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    zone.Ihnp[self.cTime] += (1-protected)*duration
                if label == 'R' :
                    zone.Rhc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    zone.Rhnp[self.cTime] += (1-protected)*duration
                if label == 'S' :
                    zone.Shc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                if label == 'E' :
                    zone.Ehc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
        return listI #à améliorer en retournant (listI, listR) SI BESOIN
            
    def initZones(self, endemicites):
        for idZ, zone in self.zones.iteritems():
            zone.setK(endemicites[idZ], self.cTime)
            zone.setParameters(endemicites[idZ])
        
               
    
    def updateHumans(self):
        
        for j in range(1, self.M+1, 1):
            
            humanId = "H"+str(j)
            human = self.humans[humanId]
            #print "time="+str(self.cTime)+" (update human) = "+humanId+", "+str(human.getState(self.cTime))+"  "+str(self.cTime)+" pse = "+str(self.pse[humanId][self.cTime])
            path = human.getPath(self.cTime)
            
            #######################################
            # calcul de la Force d'infection agrégée
            lambdaVH = 0
            for idZ, duration in path :
                lambdaVH += self.zones[idZ].getLambdaVH(self.cTime) * duration
                
            human.setLambdaVH(lambdaVH, self.cTime) 
            
            ############################
                  
            latencyP = human.getLatencyH()
            infectiousP = human.getInfectiousH()
            imuneP = human.getImuneH()
            
            
            #=============  MODELE A ETAT =====================================
            #==================================================================
            ############################################################################
            #          MISE À JOUR DE L'ÉTAT
            ############################################################################
        
            #print "mise a jour etat a t= "+str(self.cTime)
                           
            label = human.getState(self.cTime).getLabel()
            counter = human.getState(self.cTime).getCounter()
            
            protected = human.getProtected(self.cTime)
            pse = human.getPse(self.cTime)
            pse = pse + (1-protected)*lambdaVH*(1 - pse)
            
            if label == 'S':
                if (pse >= human.threshold):
                    human.setState(Etat('E', 0), self.cTime+1)
                    human.setPse(0, self.cTime+1)
                    self.zones[self.residences[humanId]].Eh0[self.cTime+1] +=1
                    self.zones[self.residences[humanId]].Ehr[self.cTime+1] +=1
                    self.listE0[self.cTime+1].append(humanId)
                else :
                    human.setPse(min(pse, 1), self.cTime+1)
                    counter +=1
                    human.setState(Etat('S', counter), self.cTime+1)
                    self.zones[self.residences[humanId]].Shr[self.cTime+1] +=1
            
            if label == 'E':
                human.setPse(0, self.cTime+1)
                if counter+1 < latencyP :
                    counter +=1
                    human.setState(Etat('E', counter), self.cTime+1)
                    self.zones[self.residences[humanId]].Ehr[self.cTime+1] +=1
                else :
                    human.setState(Etat('I', 0), self.cTime+1)
                    self.zones[self.residences[humanId]].Ihr[self.cTime+1] +=1
                    
                    
            if label == 'I':
                human.setPse(0, self.cTime+1)
                if counter+1 < infectiousP :
                    counter +=1
                    human.setState(Etat('I', counter), self.cTime+1)
                    self.zones[self.residences[humanId]].Ihr[self.cTime+1] +=1
                    
                else :
                    human.setState(Etat('R', 0), self.cTime+1)
                    self.zones[self.residences[humanId]].Rhr[self.cTime+1] +=1
                    
                    
            if label == 'R':
                human.setPse(0, self.cTime+1)
                if counter+1 < imuneP :
                    counter +=1
                    human.setState(Etat('R', counter), self.cTime+1)
                    self.zones[self.residences[humanId]].Rhr[self.cTime+1] +=1
                    
                else :
                    human.setState(Etat('S', 0), self.cTime+1)
                    self.zones[self.residences[humanId]].Shr[self.cTime+1] +=1
                
            ##############################
            
            
            #mise à jour du trajet - DANS LE CAS où IL NE CHANGE PAS
            #human.setPath(path, self.cTime+1)
            
            #par défaut le degré de protection reste le même 
            human.setProtected(protected, self.cTime+1)
            
            human.setTime(self.cTime+1)
            
    def updateZones(self):
        '''
        Calcule les FOIs en fonction des états et durées de séjour des individus
        ATTENTION : ICI ON MODIFIE LES DONNÉES. IL FAUT INTRODUIRE LA TEMPORALITÉ
        
        '''
        for i in range(1, self.N+1, 1):
            
            zoneId = "Z"+str(i)
            zone = self.zones[zoneId]
            presences = zone.getPresences(self.cTime)
            
            
            
            ## initialisation personnes presentes selon etat
            zone.Nhc[self.cTime] = 0
            zone.Shc[self.cTime] = 0
            zone.Ehc[self.cTime] = 0
            zone.Ihc[self.cTime] = 0
            zone.Rhc[self.cTime] = 0
            
            zone.Ihnp[self.cTime] = 0
            zone.Rhnp[self.cTime] = 0
            
            ## initialisation des personnes résidente selon etat
            zone.Eh0[self.cTime+1] = 0
            zone.Shr[self.cTime+1] = 0
            zone.Ehr[self.cTime+1] = 0
            zone.Ihr[self.cTime+1] = 0
            zone.Rhr[self.cTime+1] = 0
            
            #mise à jour du nombre total des résidents (facultatif)
            s = zone.Shr[self.cTime]
            e = zone.Ehr[self.cTime]
            i = zone.Ihr[self.cTime]
            r = zone.Rhr[self.cTime]
            zone.Nhr[self.cTime] = s+e+i+r
                    
            
            for humanId, duration in presences :
                human = self.humans[humanId]
                protected = human.getProtected(self.cTime)
                
                #print "time (update Zone) = "+zoneId+"   "+str(self.cTime)
                ################################################
                #MISE A JOUR DES EFFECTIFS SELON L'ÉTAT AVÉRÉ (CERTAIN)
                label = human.getState(self.cTime).getLabel()
                if label == 'I' :
                    zone.Ihc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    zone.Ihnp[self.cTime] += (1-protected)*duration
                if label == 'R' :
                    zone.Rhc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    zone.Rhnp[self.cTime] += (1-protected)*duration
                if label == 'S' :
                    zone.Shc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                if label == 'E' :
                    zone.Ehc[self.cTime] += duration
                    zone.Nhc[self.cTime] += duration
                    
                    
                            
            ###################################
            #Mise à jour des forces d'infection
            
            ###################################
            #Si démoustication ici que 1 zone **********A ADAPTER POUR PLUSIEURS ZONES
            p= self.pDem
            if self.cTime == self.tDem and zoneId == self.idDem:
                zone.Nv[self.cTime] = (1-p) * zone.Nv[self.cTime]
                zone.Sv[self.cTime] = (1-p) * zone.Sv[self.cTime]
                zone.Ev[self.cTime] = (1-p) * zone.Ev[self.cTime]
                zone.Iv[self.cTime] = (1-p) * zone.Iv[self.cTime]
                
                
            Nv = zone.Nv[self.cTime] #rajouter getters
            Sv = zone.getSv(self.cTime)
            Ev = zone.getEv(self.cTime)
            Iv = zone.getIv(self.cTime)
            
            betaVH = zone.betaVH
            betaHV = zone.betaHV
            betaHVt = zone.betaHVt
            sigmaV = zone.sigmaV
            sigmaH = zone.sigmaH
            
            Nh = zone.Nhc[self.cTime] #rajouter getters
            Ih = zone.Ihnp[self.cTime]
            Rh = zone.Rhnp[self.cTime]
            
            
            bh = (sigmaV*Nv*sigmaH)/(sigmaV*Nv + sigmaH*Nh)
            lambdaVH = bh*betaVH*Iv/Nv
            
            zone.setLambdaVH(lambdaVH, time = self.cTime+1)
            
                        
            ###############################  
            #FOI par les effectifs certains
            bv = (sigmaV*sigmaH*Nh)/(sigmaV*Nv + sigmaH*Nh)
            lambdaHV = bv*(betaHV*Ih/Nh + betaHVt*Rh/Nh)
            zone.setLambdaHV(lambdaHV, self.cTime+1)
            
           
            ################
            #Mise à jour des populations
            #Moustiques :
            nu = 1./zone.latencyV
            
            fv = zone.mu1V + Nv*zone.mu2V
            
            sv = zone.psiV*Nv + Sv - lambdaHV*Sv - Sv*fv
            ev = Ev + lambdaHV*Sv - nu*Ev - Ev*fv
            iv = Iv + nu*Ev - Iv*fv
            
            zone.setSv(sv, self.cTime+1)
            zone.setEv(ev, self.cTime+1)
            zone.setIv(iv, self.cTime+1)
            zone.setNv(sv+ev+iv, self.cTime+1) #ajouter setters
            
            #mise à jour des présences - DANS NOTRE CAS elles NE CHANGENT PAS
            #sauf evenement particulier
            # PEUT ETRE ADAPTÉ SELON LES BESOINS
            zone.setTime(self.cTime+1)
            zone.setK(zone.getK(self.cTime), self.cTime+1)
            
            
            '''
            if not(self.eventTime == self.cTime +1 and self.event == True) :
                zone.setPresence(presences, self.cTime+1)
            if self.cTime == self.eventTime :
                zone.setPresence(zone.getPresences(0), self.cTime+1)
            '''
        
    def updateModel(self):
        print "dans updateModel :"+ str(self.cTime)
        self.listE0[self.cTime+1] = []
        self.updateZones()
        self.updateHumans()
        self.setCurrentTime(self.cTime+1)
        
    def __str__(self):
        if self.N == 1 :
            zones = "zone"
        else :
            zones = "zones"
        return "Modele avec "+str(self.N)+" "+str(zones)+" et "+str(self.M)+" individus connectes\n"
        
