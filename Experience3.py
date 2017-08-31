#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:31:12 2017

@author: khiri
"""

'''
DANS CETTE EXPERIENCE ON SE FOCALISE SUR LA ZONE DE RENCONTRE. lA ZONE DE RÉSIDENCE NE
NOUS INTERESSE PAS ET NE REFLETE EN AUCUN CAS UNE SITUATION RÉELLE (DUE AUX MODIFICATIONS)
A T=100 DES ÉTATS DES INDIVIDUS

LES DONNEES ONT ÉTÉ GÉNÉRÉE PAR : exp3_generateur.py

'''

from generateur import generateur1, generateur2, setDeplacements2Zones1PR
#from ModeleProba import Modele
from ModeleEtat3 import Modele
import cPickle as pickle
from Traces import lireTraces
from PlotZoneProba import *
from Etat import Etat
import random

#nombre de zones
N = 2
#nombre de points de rencontre PR
pointRencontre = 1
#nombre d'individus
M=1000
tauxH_PR = 0.
tauxDeplacement = 0.5
#Durée passée hors du lieu de résidence
tauxSejour = 0.4




listI=[]
#nombre de pas de temps
nbStep = 100
#jour de la demoustication
tDem = 100


path  = "./Experience3/etape1/"
fic = path+"traces0.txt"

N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites = lireTraces(fic)

#permet de générer les mêmes seuil d'exposition des individus d'un test à l'autre
g = random.Random()
g.seed(1)
m = Modele(N, M, g = g)
m.residences = residence
m.initZones(endemicites)
zones = m.getZones()
humans = m.getHumans()
humansList = humans.keys()


#initialisation d'une seule personne parmi les mobile en I
listI.append(listIndMobiles[0])
#listI.extend(listIndMobiles[0:10])
m.initStatesAndProba2(listI)
m.tDem = 100
m.pDem = 0.95
m.idDem = 'Z1'

while m.cTime <= nbStep :
    t= m.cTime
    print "T == "+str(t)
    #initialisation des déplacements
    m.initTravels(paths, presences)
    m.updateModel()

fic = path + "initModele.p"
fh = open (fic, 'wb')
pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)
fh.close()


# ÉTAPE 2 DE L'EXPERIENCE : TESTER DIFFRENTS TAUX D'INFECTIEUX
cTime = 100
nbStep2 = 200

path2 = "./Experience3/etape2/"
if not os.path.exists(path2):
    os.makedirs(path2)



for i in range(11):
    if i != 10 :
        listInfected = listIndMobiles[0:(i*50)]
        listSusceptible = listIndMobiles[(i*50):]
    else :
        listInfected = listIndMobiles
        listSusceptible = []
        
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
    for idh in listSusceptible :
        humans2[idh].setState(Etat('S',0), cTime)
        humans2[idh].setProtected(1, cTime)
        humans2[idh].setPse(0, cTime)
        
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
    plot_V(zone,"")
