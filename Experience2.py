#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:36:56 2017

@author: khiri
"""

#from generateur import generateur1, generateur2
#from Traces import stockerTraces, lireTraces
#from ModeleProba import Modele
from ModeleEtat3 import Modele
import cPickle as pickle
#from Traces import lireTraces
from PlotZone import *
import random
import os

tStop = 10

#nombre de pas de temps
nbStep = 100
#nombre de zones
N = 2
#nombre de points de rencontre PR
pointRencontre = 1
#nombre d'individus
M=1001
#Sera fait 'à la main' sans tenir compte de la valeur
tauxH_PR = 0.
#Sera fait 'à la main' sans tenir compte de la valeur
tauxDeplacement = 0.1
#Durée passée hors du lieu de résidence
tauxSejour = 0.4


#nombre d'individus mobile
nbMobile = int(M*tauxDeplacement)
#liste de liste d'individus mobiles
llMobiles = []
#initialisation des liste de déplacements
lPaths = []
lPresences = []

#1ere situation : 10 personnes différente chaque jour
path  = "./Experience2/Etat/"
if not os.path.exists(path):
    os.makedirs(path)



def setDeplacements2Zones1PR(zones, humans, listeMobiles, tauxSejour, idHpr, idPR = None) :
    '''
    POUR 2 ZONES 1 POINT DE RENCONTRE
    LE POINT DE RENCONTRE EST LA PREMIERE ZONE PAR DEFAUT
    
    idHpr : identifiants des individu de la zone de rencontre (liste) 
    '''
    residences = {}
    idZones = zones.keys()
    #print idZones
    if idPR is None :
        idPR = idZones[0]
        idZ = idZones[1]
    else :
        #print idPR
        idZ = idZones.remove(idPR)
        idZ = idZones[0]
        #print idZ
    presences = {}
    presences[idZ]=[]
    presences[idPR]=[]
    paths = {}
    for idH in humans.keys():
        paths[idH]=[]       
        if idHpr.__contains__(idH):
            print "hourra!!!!!"
            paths[idH].append((idPR, 1))
            print "idPR ="+idPR
            print "id = "+idH
            presences[idPR].append((idH,1))
            print presences
            residences[idH]=idPR
        else :
            if listeMobiles.__contains__(idH):
                paths[idH].extend([(idPR,tauxSejour), (idZ, 1-tauxSejour)])
                presences[idPR].append((idH, tauxSejour))
                presences[idZ].append((idH, 1-tauxSejour))
                residences[idH]=idZ
            else :
                paths[idH].append((idZ, 1))
                presences[idZ].append((idH,1))
                residences[idH]=idZ
    return paths, presences, residences
    
#permet de générer les mêmes seuil d'exposition des individus d'un test à l'autre
g = random.Random()
g.seed(1)
m = Modele(N, M, g = g)

zones = m.getZones()
humans = m.getHumans()
humansList = humans.keys()

#liste des résident dans PR
idHpr = ['H1001']
#zone de rencontre
idPR = 'Z1'

i=0
k=0
for j in range(nbMobile, M, nbMobile):
    print "i="+str(i)
    print "j= "+str(j)
    lMobiles = humansList[i:j]
    llMobiles.append(lMobiles)
    i=j
    paths, presences, residences = setDeplacements2Zones1PR(zones, humans, lMobiles, tauxSejour, idHpr, idPR)
    lPaths.append(paths)
    lPresences.append(presences)
    k +=1


#initialisation des endemicites
endemicites={}
endemicites['Z1']= 1.
endemicites['Z2']= 0.5
m.initZones(endemicites)

#initialisation du lieu de résidence
m.residences = residences

listI = ['H1001']
m.initStatesAndProba2(listI)

m.initTravels(lPaths[0], lPresences[0])

paths2, presences2 = generateur2(residences)

###########################################################################
#                    TEST 1
###########################################################################
#initialisation de la proportion de moustiques infectés à 80% dans la zone de rencontre
#revient à initialiser sa force d'infection à 0.50
zones['Z1'].Iv[0] = 80


size = len(lPaths)
while m.cTime < nbStep :
    t= m.cTime
    print "T == "+str(t)
    #initialisation des déplacements
    if t<=tStop :
        groupe = t%size
        m.initTravels(lPaths[groupe], lPresences[groupe])
    else :
        m.initTravels(paths2, presences2)
    m.updateModel()

rep = path + "10persDiff/"
if not os.path.exists(rep):
    os.makedirs(rep)
    
fic = rep+ str(N)+"zones_"+str(M)+"Individus_"+str(pointRencontre)+"pointRencontre_deplacement"+str(tauxSejour)+".p"

fh = open (fic, 'wb')

pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)

fh.close()


###########################################################################
#                    TEST 2
###########################################################################
g.seed(1)
m2 = Modele(N, M, g)

zones2 = m2.getZones()
humans2 = m2.getHumans()
humansList = humans2.keys()

#liste des résident dans PR
idHpr = ['H1001']
#zone de rencontre
idPR = 'Z1'


#initialisation des endemicites
endemicites={}
endemicites['Z1']= 1.
endemicites['Z2']= 0.5
m2.initZones(endemicites)

#initialisation du lieu de résidence
m2.residences = residences

listI = ['H1001']
m2.initStatesAndProba2(listI)

m2.initTravels(lPaths[0], lPresences[0])

##############################
#initialisation de la proportion de moustiques infectés à 80% dans la zone de rencontre
#revient à initialiser sa force d'infection à 0.50
zones2['Z1'].Iv[0] = 80



while m2.cTime < nbStep :
    t= m2.cTime
    print "T == "+str(t)
    #initialisation des déplacements
    if t<=tStop :
        m2.initTravels(lPaths[0], lPresences[0])
    else :
        m2.initTravels(paths2, presences2)
    m2.updateModel()

rep2 = path + "10persIdentiq/"
if not os.path.exists(rep):
    os.makedirs(rep)
    
fic = rep2+ str(N)+"zones_"+str(M)+"Individus_"+str(pointRencontre)+"pointRencontre_deplacement"+str(tauxSejour)+".p"

fh = open (fic, 'wb')

pickle.dump(m2,fh,pickle.HIGHEST_PROTOCOL)

fh.close()



plot_AllPropIH(zones, rep, tauxSejour)
plot_AllPropEHr(zones, rep, tauxSejour)
plot_AllPropE0(zones, rep, tauxSejour)
cumul1 = np.sum(zones['Z2'].Eh0.values())

plot_AllPropE0(zones2, rep2, tauxSejour)
plot_AllPropIH(zones2, rep2, tauxSejour)
plot_AllPropEHr(zones2, rep2, tauxSejour)
cumul2 = np.sum(zones2['Z2'].Eh0.values())

print cumul1
print cumul2
