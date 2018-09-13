#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:33:17 2017

@author: khiri
"""

#genère données à tester sur les differents types de modèles

from generateur import generateur1Bis
from Traces import stockerTraces
import os
#Entrez le nombre de zones à considérer, SVP : 
N = 2
#Entrez le nombre de zones de rencontres à considérer, SVP : 
pointRencontre = 1 
#"Entrez le nombre d'individus à considérer, SVP : ")
M = 1000

#"Entrez le taux d'individus résidents dans des zones de rencontre : "
tauxH_PR=0.001


    
#"Entrez le taux de déplacement retenu pour le modèle, SVP.\nIl représente le taux d'individus non résidant dans une zone de rencontre qui se déplacent :")
tauxDeplacement = 0.2
    
#Entrez le taux de séjour des individus retenu pour le modèle, SVP.\nTapez None si vous souhaitez qu'il soit généré aléatoirement pour chaque individu : ") 
tauxSejour =0.5
 
# si taux de séjour aléatoire décommneter la ligne suivante et commentez la précédente
   # tauxSejour = None

#endem = raw_input("Souhaitez-vous entrer vous-même les endémicités des zones ? O/N : ")
#print endem
#endem = endem[0]
#while (endem != 'O' and endem != 'o' and endem != 'N' and endem != 'n') :
#    endem = raw_input("Veuillez répondre par 'O' ou 'o' pour oui, 'N' ou 'n' pour non :")
#if endem == 'N' or endem == 'n' :
#    endemicite = None
#else :
#    endemicite = 0 #valeur quelconque
    
repartition, residence, paternsIndividus, listIndMobiles, paths, presences = generateur1Bis(N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour)

endemicites={}
#Endemicités des zones de rencontre d'abord. Ajoutez autant de lignes que de zones de rencontre
endemicites['Z1']=0.8
#endemictés des zones de résidences. Ajoutez autant de lignes que de zones de résidences
endemicites['Z2']=0.2

path= "./DV/"+str(N)+"Zones"+str(pointRencontre)+"PR/test0/"
# "Entrez le chemin du fichier  ou vous souhaitez stocker la trace, SVP : ")
if not os.path.exists(path):
    os.makedirs(path)
#    
 
pathFic = path+'/traces0.txt'

stockerTraces(pathFic, N, M, pointRencontre, tauxH_PR, tauxDeplacement, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites)
        
