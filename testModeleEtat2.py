#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:26:11 2017

@author: khiri
"""

from ModeleEtat3 import Modele
from generateur import generateur2
import cPickle as pickle
from Traces import lireTraces
import os



nbStep = 2
N =5
pointRencontre = 2
tauxDeplacement = 1

#choix du numéro de test
debut = 3
nbTest= 4

listI = []

#for i in range(nbTest):
for i in range(debut,nbTest,1):
    chemin  = "./"+str(N)+"Zones"+str(pointRencontre)+"PR/test"+str(i)+"/"
    print chemin
    if not os.path.exists(chemin):
        os.makedirs(chemin)
    
    traces = chemin+"traces"+str(i)+".txt"
    
    #chargement des traces de déplacements
    N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites  = lireTraces(str(traces))
    
        
    m = Modele(N, M)
    m.initTravels(paths, presences)
    m.initZones(endemicites)
    m.FBwithProba = False
    m.residences = residence
    
    '''
    #lieux de résidence :
    (H420, Z3)
    (H911, Z5)
    (H578, Z4)
    (H10, Z1)
    (H189, Z2)
    '''
    if i == 2 :
        listI = ['H420','H911','H578']
    if i == 3 :
        listI = ['H10','H189']

        
    
    '''
    fic = chemin+"listI.p"
    if os.fic.exist() :
        fh = open(fic)
        listI  = pickle.load(fh)
        fh.close()
    '''
    if len(listI) == 0:
        listI = m.initStatesAndProba(0.05)[0]

    else :
        m.initStatesAndProba2(listI)
    
        fh = open (fic, 'wb')
        pickle.dump(listI,fh,pickle.HIGHEST_PROTOCOL)
        fh.close()

    humans = m.getHumans()
    zones = m.getZones()
    
    while m.cTime < nbStep :
        t= m.cTime
        print "T == "+str(t)
        m.initTravels(paths, presences)
        m.updateModel()
    
    
    rep = chemin + "ModeleEtat3/"
    if not os.path.exists(rep):
        os.makedirs(rep)
        
    fic = rep+ str(N)+"zones_"+str(M)+"Individus_"+str(pointRencontre)+"pointRencontre_0.5deplacement.p"
    
    fh = open (fic, 'wb')
    
    pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)
    
    fh.close()
       
    #####################################################################################
    #                 SANS DÉPLACEMENT
    #####################################################################################
    print "nombre de zones : "+str(N)
    print "nombre d'individus : "+str(M)
    print "nombre de points de rencontre :"+str(pointRencontre)
    print "taux d'individus habitants aux points de rencontres :"+str(alpha)
    print "taux de déplacement :" +str(tauxDeplacement)
    print
    
    paths2, presences2 = generateur2(residence)
    m2 = Modele(N, M)
    m2.initTravels(paths2, presences2)
    m2.initZones(endemicites)
    m2.residences = residence
    m2.FBwithProba = False
    
    #initialisation ALEATOIRE de la proportion des infectieux
    #m2.initStatesAndProba(0.5) 
    m2.initStatesAndProba2(listI)
    
    humans2 = m2.getHumans()
    zones2 = m2.getZones()
    
    while m2.cTime < nbStep :
        t= m2.cTime
        print "T == "+str(t)
        m2.initTravels(paths2, presences2)
        m2.updateModel()
        print "fin d'un test"
    
    
    
    fic2 = rep+ str(N)+"zones_"+str(M)+"Individus_"+str(pointRencontre)+"pointRencontre_PASdeplacement.p"
    
    fh2 = open (fic2, 'wb')
    
    pickle.dump(m2,fh2,pickle.HIGHEST_PROTOCOL)
    
    fh2.close()
    
    listI = [] #remise à zero de listI
    
    


'''
#affichage du modèle
print
print
print "====================== VALEURS INTEGRÉE DANS LE MODÈLE ========================="
print "--------------------Individus----------"

for j in range(1, m.getNbHumans()+1, 1):
    humanId = "H"+str(j)
    print humans[humanId]
    print "---------------"
   
print "--------------------Zones--------------"

for i in range(1, m.getNbZones()+1, 1):
    zoneId = "Z"+str(i)
    print zones[zoneId]
    print "---------------"
'''
