#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 16:30:24 2017

@author: khiri
"""


def stockerTraces(path, N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternsIndividus, listIndMobiles, paths, presences, endemicites) :
    fichier = open(path,"w") 
    
    
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
    print "taux de séjour :" +str(tauxSejour)
    fichier.write("#taux de séjour :\n" +str(tauxSejour)+"\n")
    
    print
    fichier.write("#\n")
    
    
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
    
    
def lireTraces(path):
    
    fic = open(path,"r")
    
    line = fic.readline()
    line = fic.readline()
    N = int(line)
    #print "nombre de zones : "+str(N)
    
    line = fic.readline()
    line = fic.readline()
    M = int(line)
    #print "nombre d'individus : "+str(M)
    
    
    line = fic.readline()
    line = fic.readline()
    pointRencontre = int(line)
    #print "nombre de points de rencontre :"+str(pointRencontre)
    
    line = fic.readline()
    line = fic.readline()
    alpha = float(line)
    #print "taux d'individus habitants aux points de rencontres :"+str(alpha)
    
    line = fic.readline()
    line = fic.readline()
    seuil = float(line)
    #print "taux de déplacement :" +str(seuil)
    
    line = fic.readline()
    line = fic.readline()
    tauxSejour = float(line)
    print "taux de séjour :" +str(tauxSejour)
    
    line = fic.readline()
    line = fic.readline()
    line = fic.readline()
    residence = {}
    while (line != "#\n"):
        s = line[1:-2].split(", ")
        residence[s[0]] = s[1]
        line = fic.readline()
    '''   
    print "lieux de résidence :"
    for k, v in residence.iteritems():
        print (k, v)
    '''
    line  = fic.readline()
    while (line != "#patron de déplacements :\n"):
        line = fic.readline()
    
    paternIndividus = {}  
    line = fic.readline()
    while (line != "#\n"):
        s = line[1:-2].split(", (")
        idh = s[0]
        liste = s[1].split(", [")
        ll = []
        for e in liste[1][:-2].split(", "):
            ll.append(e)
        lll = liste[0].split(", ")
        lll[1] = float(lll[1])
        lll[2] = float(lll[2])
        lll.append(ll)
        paternIndividus[idh] = (lll[0], lll[1], lll[2], lll[3])
        
        line = fic.readline()
    '''    
    print "patron de déplacements :"
    for k, v in paternIndividus.iteritems():
        print (k, v)    
    '''
    line  = fic.readline()
    while (line != "#liste des individus mobiles\n"):
        line = fic.readline()
    listIndMobiles = []
    line = fic.readline()
    line2 = line[1:-2].split(", ")
    for e in line2 :
        listIndMobiles.append(e[1:-1])
    '''    
    print "liste des individus mobiles"
    print(listIndMobiles)
    '''
    
    line  = fic.readline()   
    while (line != "#paths\n"):
        line = fic.readline()
        
    paths = {}
    line = fic.readline()
    while (line != "#\n"):
        
        s = line[1:-3].split(", [")
        p = []
        s2 = s[1][1:-1].split("), (")
        for s3 in s2 :
            ss = s3.split(", ")
            p.append((ss[0][1:-1], float(ss[1])))
            paths[s[0]] = p
            
        line = fic.readline()
    '''    
    print "paths"
    for k, v in paths.iteritems():
        print (k, v)
    '''    
    while (line != "#presences\n"):
        line = fic.readline()
        
    presences = {}
    line = fic.readline()
    
    while (line != "#\n"):
        
        s = line[1:-3].split(", [")
        p = []
        s2 = s[1][1:-1].split("), (")
        for s3 in s2 :
            ss = s3.split(", ")
            p.append((ss[0][1:-1], float(ss[1])))
            presences[s[0]] = p
            
        line = fic.readline()
    '''
    print "presences"
    for k,v in presences.iteritems():
        print (k, v)
    '''    
    while (line != "#liste des endémicités :\n"):
        line = fic.readline()
        
    endemicites = {}
    line = fic.readline()
    while (line != "#\n"):
        s = line[1:-2].split(", ")
        endemicites[s[0]] = float(s[1])
        line = fic.readline()
        if line == '' : break
    '''
    print "liste des endémicités :"
    for k, v in endemicites.iteritems():
        print (k, v)
    '''   
    fic.close()
    
    return N, M, pointRencontre, alpha, seuil, tauxSejour, residence, paternIndividus, listIndMobiles, paths, presences, endemicites

