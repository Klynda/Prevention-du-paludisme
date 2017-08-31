#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:45:37 2017

@author: khiri
"""
import random


def setDeplacements2Zones1PR(zones, humans, listeMobiles, tauxSejour, idHpr, idPR = None) :
    '''
    POUR UNE LISTE D'INDIVIDUS MOBILES BIEN DÉFINIS
    
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

#GENERATION DES LIEU DE RÉSIDENCES

def generateur1(N, M, pointRencontre, alpha, seuil, Qs = None, endemicites = None):
    #initialisation nbre de zones
    n = N
    
    #initialisation nbre d'humains
    m= M
    
    #initialisation nbre de point de rencontre
    pr = pointRencontre
    
    #pourcentation population pr
    pppr = alpha
    
    #lieu de résidence de chaque individu
    residence={}
    
    ###################################################################
    #répartition du nombre d'individus sur les zones de regrouprement
    repartition ={}
    
    # nbre d'individu par zones de rencontre
    if pr != 0 :
        #population pr
        popPr = int(pppr * m)
        nbIndPr = popPr / pr
        k = 1
        for i in range(pr-1):
            listInd = []
            identifiant = 'Z'+str(i+1)
            for j in range(nbIndPr) :
                listInd.append('H'+str(k))
                residence['H'+str(k)] = identifiant
                k +=1
            repartition[identifiant] = listInd
        if pr != 0:
            identifiant = 'Z'+str(pr)
            listInd = []
            for j in range(nbIndPr + popPr % pr) :
                listInd.append('H'+str(k))
                residence['H'+str(k)] = identifiant
                k +=1
        repartition[identifiant] = listInd
    else :
        popPr = 0
        k = 1
    #print "popPr = " +str(popPr)   
    
    ############################################################
    #répartition sur les zones restantes
    
    #nb de zones restantes
    zr = n - pr
    
    
    #nb d'individus dans le reste des zones
    popZ = m - popPr
    
    
    #nbre d'individus par zones restantes
    if zr != 0 :
        nbIndZ = popZ / zr
    

    
        for i in range(pr, n, 1):
            listInd = []
            identifiant = 'Z'+str(i+1)
            for j in range(nbIndZ):
                listInd.append('H'+str(k))
                residence['H'+str(k)] = identifiant
                k +=1
            repartition[identifiant] = listInd
        
        listInd = []
        identifiant = 'Z'+str(n)
        for j in range(popZ % zr) :
            listInd.append('H'+str(k))
            residence['H'+str(k)]=identifiant
            k +=1
        repartition['Z'+str(n)] = listInd
    
    ########################################################
    #Calcul du patern pour chaque individu
    path = {}
    presences = {}
    paternsIndividus = {}
    listIndMobiles = []
    
    for idH, idZ in residence.iteritems():
        pd = random.random()
        if Qs is None :
            qs = random.random()
        else :
            qs = Qs
        prChoisis = []
        path[idH] = []
        
        #----------------------
        lpr = range(1, pr+1, 1)
        listPr = []
        for li in lpr :
            listPr.append('Z'+str(li))
        #----------------------
       
            
        if not(listPr.__contains__(idZ)) :
            if pd<= seuil and pr != 0 :
                 #ajout du ratio temps dans la zone de résidence
                if presences.__contains__(idZ) :
                    presences[idZ].append( (idH, 1 - qs) )
                else :
                    presences[idZ] = [(idH, 1 - qs)]
                path[idH].append( (idZ, 1 - qs) )
                
                #jouter l'individu dans la liste des mobiles
                listIndMobiles.append(idH)
                
                #si la valeur est supérieure au seuil choisir uniformement un 
                #nombre de point de rencontre parmi ceux connus
                nbpr = random.randint(1, pr)
                
                #liste des points de rencontre disponibles
                listPr = range(1, pr+1, 1)
                #liste des points de renbcontre choisis
                for i in range (nbpr):
                    j = random.randint(0, len(listPr)-1) #il s'agit d'un indice
                    zChoisie = 'Z'+str(listPr.pop(j))
                    prChoisis.append(zChoisie)
                    path[idH].append( (zChoisie, qs/nbpr) )
                    if presences.__contains__(zChoisie) :
                        presences[zChoisie].append((idH, qs/nbpr))
                    else :
                        presences[zChoisie] = [(idH, qs/nbpr)]
            else :
                path[idH]= [(idZ, 1)]
                if presences.__contains__(idZ) :
                    presences[idZ].append( (idH, 1) )
                else :
                    presences[idZ] = [(idH, 1)]
        else :
            prChoisis = []
            path[idH]= [(idZ, 1)]
            if presences.__contains__(idZ) :
                presences[idZ].append( (idH, 1) )
            else :
                presences[idZ] = [(idH, 1)]
        paternsIndividus[idH] = (idZ, pd, qs, prChoisis)
        
    ######################################################
    
    #liste des endémicités : est représentée par un dictionnaire {idZ : K}
    endemicite = {}
    
    #valeurs extrèmes pour les points d'interêts (K=0 ou K=1) on alterne entre les zones
    for i in range(pr):
        identifiant = 'Z'+str(i+1)
        if endemicites is None :
            endemicite[identifiant] = 1 - i%2
        else :
            endem = input("Entrez l'endémicité de la zone de rencontre "+identifiant+", SVP : ")
            while (endem < 0 or endem >1) :
                endem = input("La valeur doit être comprise entre 0 et 1 : ")
            endemicite[identifiant] = endem
        
    #pour le reste des zones valeur aléatoire entre 0 et 1
    for i in range(pr, n, 1):
        identifiant = 'Z'+str(i+1)
        if endemicites is None :
            endemicite[identifiant] = random.random()
        else :
            endem = input("Entrez l'endémicité de la zone de résidence "+identifiant+", SVP : ")
            while (endem < 0 or endem >1) :
                endem = input("La valeur doit être comprise entre 0 et 1 : ")
            endemicite[identifiant] = endem
    
    
    
    
    return repartition, residence, paternsIndividus, listIndMobiles, path, presences, endemicite

#generes path et prtesences si pas de déplacements
def generateur2(residence) :
    path = {}
    presences = {}
    for idH, idZ in residence.iteritems():
        
        path[idH]= [(idZ, 1)]
        if presences.__contains__(idZ) :
            presences[idZ].append( (idH, 1) )
        else :
            presences[idZ] = [(idH, 1)]
    return path, presences

'''
N = 3
M = 9
pointRencontre = 1
alpha = 0.2
seuil = 0.5

fichier = open("testfile.txt","w") 


print "nombre de zones : "+str(N)
fichier.write("#nombre de zones : \n"+str(N)+"\n")
print "nombre d'individus : "+str(M)
fichier.write("#nombre d'individus : \n"+str(M)+"\n")
print "nombre de points de rencontre :"+str(pointRencontre)
fichier.write("#nombre de points de rencontre :\n"+str(pointRencontre)+"\n")
print "taux d'individus habitants aux points de rencontres :"+str(alpha)
fichier.write("#taux d'individus habitants aux points de rencontres : \n"+str(alpha)+"\n")
print "taux de déplacement :" +str(seuil)
fichier.write("#taux de déplacement :\n" +str(seuil)+"\n")
print
fichier.write("#\n")

print "============================ VALEURS GÉNÉRÉES ==========================="
repartition, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites= generateur1(N, M, pointRencontre, alpha, seuil)



print "lieux de résidence :"
fichier.write("#lieux de résidence :\n")
for k, v in residence.iteritems():
    print (k, v)
    fichier.write("("+str(k)+", "+str(v)+")\n")
print
fichier.write("#\n")
print "patron de déplacements :"
fichier.write("#patron de déplacements :\n")
for k, v in paternsIndividus.iteritems():
    print (k, v)
    fichier.write("("+str(k)+", "+str(v)+")\n")
print
fichier.write("#\n")
print "liste des individus mobiles"
fichier.write("#liste des individus mobiles\n")
print(listIndMobiles)
fichier.write(str(listIndMobiles)+"\n")
print
fichier.write("#\n")
print "paths"
fichier.write("#paths\n")
for k, v in paths.iteritems():
    print (k, v)
    fichier.write("("+str(k)+", "+str(v)+")\n")
print
fichier.write("#\n")
print "presences"
fichier.write("#presences\n")
for k,v in presences.iteritems():
    print (k, v)
    fichier.write("("+str(k)+", "+str(v)+")\n")
    print

fichier.write("#\n")
print "liste des endémicités :"
fichier.write("#liste des endémicités :\n")
for k, v in endemicites.iteritems():
    print (k, v)
    fichier.write("("+str(k)+", "+str(v)+")\n")

fichier.close() 

print "============================ VALEURS GÉNÉRÉES ==========================="
paths2, presences2 = generateur2(residence)

print
print "paths"
for k, v in paths2.iteritems():
    print (k, v)
print
print
print "presences"
for k,v in presences2.iteritems():
    print (k, v)
    print

'''