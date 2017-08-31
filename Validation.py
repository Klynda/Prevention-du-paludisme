#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:26:11 2017

@author: khiri
"""

from ModeleEtat3 import Modele
from generateur import generateur1, generateur2
import cPickle as pickle
from Traces import lireTraces
import os

#############################
#   TEST EFFECTUE POUR 1 ZONE
#############################

nbStep = 200
M=1000
N =1
k=0.5

nbTest= 1
for i in range(nbTest):
    repartition, residence, paternsIndividus, listIndMobiles, path, presences, endemicite = generateur1(N, M, 1, 1, 1, Qs = None)
    m = Modele(N, M)
    m.residences = residence
    paths2, presences2 = generateur2(residence)
    m.initTravels(paths2, presences2)
    
    
    #initialisation ALEATOIRE de la proportion des infectieux
    listI = ['H1']
    m.initStatesAndProba2(listI)
    m.initZones({'Z1':k})
    
    # seuil au dela duquel un individu passe à l'état exposé
    m.alpha = 0.5
    humans = m.getHumans()
    zones = m.getZones()
    
    while m.cTime < nbStep :
        t= m.cTime
        print "T == "+str(t)
        m.updateModel()
        m.initTravels(paths2,presences2)

rep = "K="+str(k)+"/"
fic = rep+"Validation/modeleEtat.p"
  
fh = open (fic, 'wb')

pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)

fh.close()

'''
from PlotZone import *
plot_AllPropIH(zones, rep, tauxSejour)
plot_AllPropEHr(zones, rep, tauxSejour)
plot_AllPropE0(zones, rep, tauxSejour)
plot_H(zones['Z1'],"")
plot_V(zones['Z1'],"")
'''