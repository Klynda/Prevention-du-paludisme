#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 11:35:15 2017

@author: khiri
"""
from generateur import generateur1, generateur2, setDeplacements2Zones1PR
#from ModeleProba import Modele
from ModeleEtat3 import Modele
import cPickle as pickle
from Traces import lireTraces
from PlotZoneProba import *
from Etat import Etat
import os

# ÉTAPE 1 DE L'EXPÉRIENCE S'APPUIE SUR L'ÉTAPE 1 DE L'EXPERIENCE 3
path  = "./Experience3/etape1/"
fic = path+"traces0.txt"

N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites = lireTraces(fic)



# ÉTAPE 2 DE L'EXPERIENCE : TESTER DIFFRENTS TAUX D'INFECTIEUX
cTime = 100
nbStep2 = 200

path2 = "./Experience4/etape2/"
if not os.path.exists(path2):
    os.makedirs(path2)


listInfected = listIndMobiles

for i in range(11):
    if i != 10 :
        listProtected = listIndMobiles[0:(i*50)]
        
    else :
        listProtected = listIndMobiles
        
    path  = "./Experience3/etape1/"
    fic = path + "initModele.p"
    fh = open(fic)
    m2 = pickle.load(fh)
    fh.close()
    
    m2.setCurrentTime(cTime)
    zones2 = m2.getZones()
    humans2 = m2.getHumans()
    
    #initialisation des états et protection (si sains)
    for idh in listInfected :
        humans2[idh].setState(Etat('I', 0), cTime)
    for idh in listProtected :
        humans2[idh].setProtected(1, cTime)
        
    while m2.cTime <= nbStep2 :
        t= m2.cTime
        print "T == "+str(t)
        #initialisation des déplacements
        m2.initTravels(paths, presences)
        m2.updateModel()
        
    
    fic2 = path2 + "zone"+str(i)+".p"
    fh2 = open (fic2, 'wb')
    pickle.dump(m2.getZones()['Z1'],fh2,pickle.HIGHEST_PROTOCOL)
    fh2.close()
    



for i in range(11):
    fic2 = path2 + "zone"+str(i)+".p"
    fh2 = open(fic2)
    zone = pickle.load(fh2)
    fh2.close()
    zones = m.getZones()
    plot_V(zone,"")
