#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:33:17 2017

@author: khiri
"""

#genère données à tester sur les differents types de modèles

from generateur import generateur1
from Traces import stockerTraces
import os

N = input("Entrez le nombre de zones à considérer, SVP : ")
pointRencontre = input("Entrez le nombre de zones de rencontres à considérer, SVP : ")
while (pointRencontre>=N) :
    pointRencontre = ("Le nombre de point de rencontre doit être inférieur au nombre de zones : ")
M = input("Entrez le nombre d'individus à considérer, SVP : ")
while (M<=0) :
    M = input("Le nombre de personne doit être positif : ")
    
tauxH_PR = input("Entrez le taux d'individus résidents dans des zones de rencontre : ")
while (tauxH_PR < 0 or tauxH_PR >1) :
    tauxH_PR = input("Ce taux doit être compris entre 0 et 1 : ")
    
tauxDeplacement = input("Entrez le taux de déplacement retenu pour le modèle, SVP.\nIl représente le taux d'individus non résidant dans une zone de rencontre qui se déplacent :")
while (tauxDeplacement < 0 or tauxDeplacement >1) :
    tauxDeplacement = input("Ce taux doit être compris entre 0 et 1 : ")
    
tauxSejour = input("Entrez le taux de séjour des individus retenu pour le modèle, SVP.\nTapez None si vous souhaitez qu'il soit généré aléatoirement pour chaque individu : ")
if tauxSejour != None :
    while (tauxSejour < 0 or tauxSejour >1) :
        tauxSejour= input("Ce taux doit être compris entre 0 et 1 : ")
else :
    tauxSejour = None

endem = raw_input("Souhaitez-vous entrer vous-même les endémicités des zones ? O/N : ")
print endem
endem = endem[0]
while (endem != 'O' and endem != 'o' and endem != 'N' and endem != 'n') :
    endem = raw_input("Veuillez répondre par 'O' ou 'o' pour oui, 'N' ou 'n' pour non :")
if endem == 'N' or endem == 'n' :
    endemicite = None
else :
    endemicite = 0 #valeur quelconque
    
repartition, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites = generateur1(N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, endemicite)

path = raw_input("Entrez le chemin du dossier ou vous souhaitez stocker la trace, SVP : ")
if not os.path.exists(path):
    os.makedirs(path)
    
fic = raw_input("Entrez le nom du fichier trace, SVP : ")
 
pathFic = path+"/"+fic

stockerTraces(pathFic, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites)
        
