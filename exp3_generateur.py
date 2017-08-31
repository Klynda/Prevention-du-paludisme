#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:17:34 2017

@author: khiri
"""


#genère données à tester sur les differents types de modèles

from generateur import generateur1
from Traces import stockerTraces
import os

N = 2
M=1000
pointRencontre = 1
tauxH_PR = 0.
tauxDeplacement = 0.5
tauxSejour = 0.4

debut = 0
nbTest= 1

###############################################################################
#               génération des données pour l'initialisation du modèle
###############################################################################

'''
for i in range(debut,nbTest,1):
    
    path  = "./experience3/etape1/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    fic = path+"traces"+str(i)+".txt"
    
    #repartition, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites = generateur1(N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour)
    N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites = lireTraces(fic)

    endemicites['Z2'] = 0.5
    
    stockerTraces(fic, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites)
    
'''

###############################################################################
#               génération des données pour les différents cas
#==============================================================================


