#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 17:47:34 2017

@author: khiri
"""

#genère données à tester sur les differents types de modèles

from generateur import generateur1
from Traces import stockerTraces
import os

N = 5
M=1000
pointRencontre = 2
tauxH_PR = 0.2
tauxDeplacement = 1
tauxSejour = 0.5

debut = 0
nbTest= 2

for i in range(debut,nbTest,1):
    path  = "./"+str(N)+"Zones"+str(pointRencontre)+"PR/test"+str(i)+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    fic = path+"traces"+str(i)+".txt"
    
    repartition, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites = generateur1(N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour)

    endemicites['Z3'] = 0.75
    endemicites['Z4'] = 0.5
    endemicites['Z5'] = 0.25
    
    stockerTraces(fic, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites)
        
