#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:01:07 2017

@author: khiri
"""

from generateur import generateur3, generateur2
from Traces import stockerTraces, lireTraces
#from ModeleProba import Modele
from ModeleEtat3 import Modele
import cPickle as pickle
from Traces import lireTraces
import random
import os

#nombre de pas de temps
nbStep = 200
#nombre de zones
N = 3
#nombre de points de rencontre
pointRencontre = 2
#nombre d'individus
M=1000

tauxH_PR = 0.
tauxDeplacement=0.5
tauxSejour=0.4

# LES DONNÉES ON DÉJÀ ÉTÉ GÉNÉRÉE ET STOCKÉE -> PLUS QU'À LIRE LE FICHIER TRACE

#repartition, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites = generateur3(N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, endemicites='0')

path  = "./Experience6/"
if not os.path.exists(path):
    os.makedirs(path)
        
fic = path+"traces.txt"

'''
#stockerTraces(fic, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites)
    
N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites = lireTraces(fic)

#permet de générer les mêmes seuil d'exposition des individus d'un test à l'autre
g = random.Random()
m = Modele(N, M, g.seed(1))
m.residences = residence
m.initZones(endemicites)
zones = m.getZones()
humans = m.getHumans()
humansList = humans.keys()


#Tous les individus sont sains
listI = []
m.initStatesAndProba2(listI)

#initialisation de la proportion de moustiques infectés à 80% dans les zones de rencontre
zones['Z1'].Iv[0] = 30
zones['Z2'].Iv[0] = 30
#Rappel : le nombre de vecteur est initialisé à 100 par défaut

fic = path+"modele_init.p"
fh = open (fic, 'wb')
pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)
fh.close()
'''

# décommenter le bloc et commenter la ligne en dessous pour changer paramètres modèle

N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites = lireTraces(fic)

#identifiants des zones à démoustiquer
idDem = ['', 'Z1', 'Z2', 'Z3']
#pour completer le nom du fichier stocké
idFic = ['', '_dem1', '_dem2', '_dem3']

for i in range(len(idDem)):
    fic = path + "modele_init.p"
    fh = open(fic)
    m = pickle.load(fh)
    fh.close()
    
    m.tDem = 12
    m.pDem = 0.95
    m.idDem = idDem[i]
    while m.cTime <= nbStep :
        t= m.cTime            
        print "T == "+str(t)
        #initialisation des déplacements
        m.initTravels(paths, presences)
        m.updateModel()
    
    #fic = path + "modele.p"
    #fic = path + "modele_dem1.p"
    #fic = path + "modele_dem2.p"
    fic = path + "modele"+idFic[i]+".p"
    fh = open (fic, 'wb')
    pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)
    fh.close()
    
    