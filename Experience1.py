#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:01:07 2017

@author: khiri
"""

from generateur import generateur1, generateur2
from Traces import stockerTraces, lireTraces
#from ModeleProba import Modele
from ModeleEtat3 import Modele
import cPickle as pickle
from Traces import lireTraces
import os

#nombre de pas de temps
nbStep = 20
#nombre de zones
N = 2
#nombre de points de rencontre
pointRencontre = 1
#nombre d'individus
M=3

for tauxSejour in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] :
    path  = "./Experience1/Sejour"+str(tauxSejour)+"/"
    if not os.path.exists(path):
        os.makedirs(path)
        
    
    traces = path+"traces"+str(tauxSejour)+".txt"
    
    #Génération et stockage des données
    #=================================
    #ATTENTION NE SERT QUE POUR FAIRE LE SQUELETTE ==> FICHIERS MODIFIÉS À LA MAIN POUR LES BESOINS DU TEST
    #LAISSER LES COMMENTAIRES!!!
    '''
    #taux d'individus par point de rencontre 
    tauxH_PR = 0. #sera ajouté manuellement dans fichier trace
    #proportion de personnes qui se déplacent
    tauxDeplacement = 0.5 #NON prise en compte car c'est toujours H1 qui se déplace

    repartition, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites = generateur1(N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour)
    
    stockerTraces(traces, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites)
    
    '''
    
    #Pour changer l'endémicité de la zone de résidence
    #============================================
    '''
    endemicites['Z2'] = 0.2
    
    stockerTraces(traces, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites)
    '''
    #Lecture des données d'initialisation
    #====================================
    N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites = lireTraces(traces)
    
    #Initialisation du modèle
    m = Modele(N, M)
    #Initialisation de l'endémicité des zones
    m.initZones(endemicites)
    #Initialisation des zones de résidences
    m.residences = residence
    #Initialidation des personnes infectés
    listI = ['H3']
    m.initStatesAndProba2(listI)
    #Récupération des variables "humains" et "zones"
    humans = m.getHumans()
    zones = m.getZones()
    
    #POUR CETTE EXPÉRIENCE ON FIXE LE SEUIL DE 'H1' à 0.5
    humans['H1'].threshold = 0.5
    
    ###########################################################################
    #Déroulement du modèle selon le nombre de jours désiré
    
    while m.cTime < nbStep :
        t= m.cTime
        print "T == "+str(t)
        #Initialisation des déplacements
        m.initTravels(paths, presences)
        m.updateModel()
    
    #Stockage du résultat dans le dossier 
    #====================================
    rep = path + "ModeleEtat/"
    if not os.path.exists(rep):
        os.makedirs(rep)
        
    fic = rep+ str(N)+"zones_"+str(M)+"Individus_"+str(pointRencontre)+"pointRencontre_deplacement"+str(tauxSejour)+".p"
    
    fh = open (fic, 'wb')
    
    pickle.dump(m,fh,pickle.HIGHEST_PROTOCOL)
    
    fh.close()