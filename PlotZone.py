#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:21:21 2017

@author: khiri
"""


import matplotlib.pyplot as plt
import numpy as np

'''
zone est une instance de la classe Zone
On récupère les différentes valeurs de Sv, Ev, Iv, ...
qui sont des dictionnaires de la forme {temps : valeur}
'''

def plot_K(zone, titre):
    fig = plt.figure()
    fig.suptitle(u"evolution de K dans le temps - Zone "+zone.getId(), fontsize=12, fontweight='bold')
    taille = len(zone.K)
    plt.plot(range(taille), zone.K.values())
    plt.legend(loc = 'best')
    plt.show()
    #fig.savefig(titre+u"evolution K dans le temps")
    
def plot_Cvh(zone, titre):
    
    fig = plt.figure()
    fig.suptitle(u"evolution de c dans le temps - Zone "+zone.getId(), fontsize=12, fontweight='bold')
    taille = len(zone.Cvh)
    plt.plot(range(taille), zone.Cvh)
    plt.legend(loc = 'lower right')
    plt.show()
    fig.savefig(titre+u"evolution c dans le temps")


def plot_deltaHV(zone, titre):
    
    fig = plt.figure()
    fig.suptitle(u"evolution de deltaHV dans le temps - Zone "+zone.getId(), fontsize=12, fontweight='bold')
    taille = len(zone.deltaHV)
    plt.plot(range(taille), zone.deltaHV)
    plt.legend(loc = 'best')
    plt.show()
    fig.savefig(titre+u"evolution deltaVH dans le temps")

def plot_lambdaVH(zones, titre):
    
    i=0
    colors=['red', 'green', 'blue']
    for idZ in zones.keys():
        fig = plt.figure()
        fig.suptitle(u"évolution lambdaVH dans le temps - Zone "+idZ, fontsize=12, fontweight='bold')
        taille = len(zones[idZ].lambdaVH)
        tailleR = len(zones[idZ].lambdaVHR)
        plt.subplot(211)
        plt.plot(range(taille), zones[idZ].lambdaVH.values(), color = colors[0], label = u"lambdaVH reelle")
        plt.legend(loc = 'best')
        plt.subplot(212)
        plt.plot(range(tailleR), zones[idZ].lambdaVHR.values(), color = colors[1], label = u"lambdaVH calculée")
        plt.legend(loc = 'best')
        plt.show()
        i +=1
        fig.savefig(titre+u"évolution lambdaVH dans le temps "+idZ)

def plot_lambdaHV(zones, titre):
    
    i=0
    colors=['red', 'green', 'blue']
    for idZ in zones.keys():
        fig = plt.figure()
    
        fig.suptitle(u"évolution lambdaHV dans le temps - Zone "+idZ, fontsize=12, fontweight='bold')
        taille = len(zones[idZ].lambdaHV)
        #moy1 = np.sum(zones[idZ].lambdaHV.values())/taille
        #moy2 = np.sum(zones[idZ].lambdaHVR.values())/taille
        plt.plot(range(taille), zones[idZ].lambdaHV.values(), color = colors[0],label = u"lambdaHV -effectifs estimés-" )
        #plt.plot(range(taille), np.ones((taille))*moy1, color = colors[0])
        plt.plot(range(taille), zones[idZ].lambdaHVR.values(), color = colors[1], label = u"lambdaHV -effectifs réels-")
        plt.legend(loc = 'upper right')
        i +=1
        
    
    fig.savefig(titre+u"évolution lambdaHV dans le temps")
    
    
def plot_H(zone, titre):
    Sh = zone.Shc.values()
    Eh = zone.Ehc.values()
    Ih = zone.Ihc.values()
    Rh = zone.Rhc.values()
    Nh = zone.Nhc.values()
    
    ps = [float(s)/n for s, n in zip(Sh, Nh)]
    pe = [float(e)/n for e, n in zip(Eh, Nh)]
    pi = [float(i)/n for i, n in zip(Ih, Nh)]
    pr = [float(r)/n for r, n in zip(Rh, Nh)]
    
    fig = plt.figure()
    #fig.suptitle(u"proportion de personnes dans la zone "+str(zone.identifier)+"\n(K="+str(zone.K[0])+")", fontsize=12, fontweight='bold')
    
    plt.plot(zone.Shc.keys(), Sh , color='blue')
    plt.plot(zone.Ehc.keys(), Eh , color='orange')
    plt.plot(zone.Ihc.keys(), Ih , color='red')
    plt.plot(zone.Rhc.keys(), Rh , color='green')
    plt.legend(('Sh', 'Eh', 'Ih', 'Rh'), loc = 'upper right')
    
    axes = plt.gca()
    axes.set_xlabel('temps en jours')
    axes.set_ylabel('nombre de personnes')
    leg = axes.get_legend()
    leg.legendHandles[0].set_color('blue')
    leg.legendHandles[1].set_color('orange')
    leg.legendHandles[2].set_color('red')
    leg.legendHandles[3].set_color('green')
    #plt.xlim(xmin = 0.)
    #plt.ylim([0,1])
    
    #fig.savefig(titre)
    #plt.close(fig)
    
    return ps, pe, pi, pr

def plot_Esperances(zone, titre):
    Es = zone.Es.values()
    Ee = zone.Ee.values()
    Ei = zone.Ei.values()
    Er = zone.Er.values()
    Nh = zone.Nhc.values()
          
    ps = [float(s)/n for s, n in zip(Es, Nh)]
    pe = [float(e)/n for e, n in zip(Ee, Nh)]
    pi = [float(i)/n for i, n in zip(Ei, Nh)]
    pr = [float(r)/n for r, n in zip(Er, Nh)]
    
    fig = plt.figure()
    #fig.suptitle(u"Esperance de personnes dans la zone "+str(zone.identifier)+"\n(K="+str(zone.K[0])+")", fontsize=12, fontweight='bold')
    
#    #ratio des esperances
#    plt.plot(zone.Shc.keys(), ps , color='blue')
#    plt.plot(zone.Ehc.keys(), pe , color='orange')
#    plt.plot(zone.Ihc.keys(), pi , color='red')
#    plt.plot(zone.Rhc.keys(), pr , color='green')


    #espearance (effectifs)
    plt.plot(zone.Shc.keys(), Es , color='blue')
    plt.plot(zone.Ehc.keys(), Ee , color='orange')
    plt.plot(zone.Ihc.keys(), Ei , color='red')
    plt.plot(zone.Rhc.keys(), Er , color='green')
    
    plt.legend(('Sh', 'Eh', 'Ih', 'Rh'), loc = 'upper right')
    
    axes = plt.gca()
    axes.set_xlabel('temps en jours')
    axes.set_ylabel('Esperances de personnes dans la zone')#+str(zone.identifier))
    leg = axes.get_legend()
    leg.legendHandles[0].set_color('blue')
    leg.legendHandles[1].set_color('orange')
    leg.legendHandles[2].set_color('red')
    leg.legendHandles[3].set_color('green')
    plt.xlim(xmin = 0.)
#    #ratio
#    plt.ylim([0,1])
    #effectifs ********************valable seulement pour 1 zone car Nh fixe
    plt.ylim([0,Nh[0]])
    
#    fig.savefig(titre)
#    plt.close(fig)
    
def plot_AllPropSH(zones):
    fig = plt.figure()
    fig.suptitle(u"proportion de personnes saines dans chaque zone", fontsize=12, fontweight='bold')
    labels = []
    for idZ in zones.keys():
        #Sh = zones[idZ].Shc.values()
        Nh = zones[idZ].Nhc.values()
        Es = zones[idZ].Es.values()
        #ps = [float(s)/n for s, n in zip(Sh, Nh)]
        es = [float(s)/n for s, n in zip(Es, Nh)]
        #plt.plot(zones[idZ].Shc.keys(), ps)
        plt.plot(zones[idZ].Es.keys(), es)
        #labels.append("Sh de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        labels.append("E(Sh) de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
    plt.legend(labels, loc = 'best')
    plt.ylim([0, 1])
    
    
    
def plot_AllPropEH(zones, rep, ts):
    fig = plt.figure()
    #fig.suptitle(u"proportion de personnes exposées dans chaque zone", fontsize=12, fontweight='bold')
    colors = ['red', 'blue', 'green', 'cyan', 'black']
    labels = []
    i=0
    for idZ in zones.keys():
        Eh = zones[idZ].Ehc.values()
        Nh = zones[idZ].Nhc.values()
        #Ee = zones[idZ].Ee.values()
        
        #pe = [float(e)/n for e, n in zip(Eh, Nh)]
        #ee = [float(s)/n for s, n in zip(Ee, Nh)]
       
        plt.plot(zones[idZ].Ehc.keys(), Eh, color = colors[i])
        #plt.plot(zones[idZ].Es.keys(), ee, color = colors[i])
        
        labels.append("Eh de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        #labels.append("zone "+idZ+" (K="+str(zones[idZ].K[0])+")") #E(Eh) de la 
        i += 1
        #plt.ylim([0, 0.04])
        
    plt.legend(labels, loc = 'best')
    fig.savefig(rep+"Eh")
    #plt.ylim([0 , 0.225])
#    if len(zones.keys())==1 :
#        ecart = [abs(p - e) for p, e in zip(pe, ee)]
#        moyenne = np.sum(ecart)/len(ecart)
#        fig = plt.figure()
#        fig.suptitle(u"Ecart entre effectif et esperance des Exposes (moy = "+str(moyenne)+")", fontsize=12, fontweight='bold')
#        plt.plot(range(len(ecart)), ecart)
#        

def plot_AllPropEHr(zones, rep, ts):
    fig = plt.figure()
    #fig.suptitle(u"proportion de personnes exposées dans chaque zone", fontsize=12, fontweight='bold')
    colors = ['red', 'blue', 'green', 'cyan', 'black']
    labels = []
    i=0
    for idZ in zones.keys():
        Ehr = zones[idZ].Ehr.values()
        Nh = zones[idZ].Nhr.values()
        #Ee = zones[idZ].Ee.values()
        
        #pe = [float(e)/n for e, n in zip(Eh, Nh)]
        #ee = [float(s)/n for s, n in zip(Ee, Nh)]
       
        plt.plot(zones[idZ].Ehr.keys(), Ehr, color = colors[i])
        #plt.plot(zones[idZ].Nhr.keys(), Nh, color = colors[i])
        labels.append("Eh de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        #labels.append("zone "+idZ+" (K="+str(zones[idZ].K[0])+")") #E(Eh) de la 
        i += 1
        #plt.ylim([0, 0.04])
    plt.legend(labels, loc = 'best')
    fig.savefig(rep+"Ehr")
    
def plot_AllPropE0(zones, rep, ts):
    fig = plt.figure()
    #fig.suptitle(u"proportion de personnes exposées dans chaque zone", fontsize=12, fontweight='bold')
    colors = ['red', 'blue', 'green', 'cyan', 'black']
    labels = []
    i=0
    for idZ in zones.keys():
        Eh0 = zones[idZ].Eh0.values()
        Nh = zones[idZ].Nhr.values()
        #Ee = zones[idZ].Ee.values()
        
        #pe = [float(e)/n for e, n in zip(Eh, Nh)]
        #ee = [float(s)/n for s, n in zip(Ee, Nh)]
       
        plt.plot(zones[idZ].Eh0.keys(), Eh0, color = colors[i])
        #plt.plot(zones[idZ].Nhr.keys(), Nh, color = colors[i])
        labels.append("E0 de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        #labels.append("zone "+idZ+" (K="+str(zones[idZ].K[0])+")") #E(Eh) de la 
        i += 1
        #plt.ylim([0, 0.04])
    plt.legend(labels, loc = 'best')
    fig.savefig(rep+"Eh0")
        
def plot_AllPropIH(zones, rep, ts):
    fig = plt.figure()
    #fig.suptitle(u"proportion de personnes infectieuses dans chaque zone", fontsize=12, fontweight='bold')
    labels = []
    for idZ in zones.keys():
        Ih = zones[idZ].Ihc.values()
        Nh = zones[idZ].Nhc.values()
        #Ei = zones[idZ].Ei.values()
       
        #pi = [float(i)/n for i, n in zip(Ih, Nh)]
        #ei = [float(s)/n for s, n in zip(Ei, Nh)]
        
        plt.plot(zones[idZ].Ihc.keys(), Ih)
        #plt.plot(zones[idZ].Ei.keys(), ei)
        #plt.ylim([0 , 0.85])
        #labels.append("Ih de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        labels.append("zone "+idZ+" (K="+str(zones[idZ].K[0])+")") #E(Ih) de la 
    plt.legend(labels, loc = 'best')
    fig.savefig(rep+"Ih")
    
def plot_AllPropRH(zones):
    
    fig = plt.figure()
    fig.suptitle(u"proportion de personnes rétablies dans chaque zone", fontsize=12, fontweight='bold')
    labels = []
    for idZ in zones.keys():
        #Rh = zones[idZ].Rhc.values()
        Nh = zones[idZ].Nhc.values()
        Er = zones[idZ].Er.values()
       
        #pr = [float(r)/n for r, n in zip(Rh, Nh)]
        er = [float(s)/n for s, n in zip(Er, Nh)]
        
        #plt.plot(zones[idZ].Rhc.keys(), pr)
        plt.plot(zones[idZ].Er.keys(), er)
        
        #labels.append("Rh de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        labels.append("E(Rh) de la zone "+idZ+" (K="+str(zones[idZ].K[0])+")")
        
    plt.legend(labels, loc = 'best')
    axes = plt.gca()
    axes.set_xlabel('temps en jours')
    axes.set_ylabel('proportion')
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
    plt.show()



def plot_EHr(zone, rep, ts):
    labels = []
    fig = plt.figure()
    Ehr = zone.Ehr.values()
     
    plt.plot(zone.Ehr.keys(), Ehr)
    idZ = zone.getId()
    #labels.append("Eh de la zone "+idZ+" (K="+str(zone.K[0])+")")
   
    #plt.legend(labels, loc = 'best')
    axes = plt.gca()
    axes.set_xlabel('time (day)')
    axes.set_ylabel('number of exposed people')
    fig.savefig(rep+"zone"+idZ+"_Ehr")
    
    
def plot_EH0(zone, rep, ts):
    labels = []
    fig = plt.figure()
    Eh0 = zone.Eh0.values()
     
    plt.plot(zone.Eh0.keys(), Eh0)
    idZ = zone.getId()
    #labels.append("E0 de la zone "+idZ+" (K="+str(zone.K[0])+")")
   
    #plt.legend(labels, loc = 'best')
    axes = plt.gca()
    axes.set_xlabel('time (day)')
    axes.set_ylabel('number of new exposed people')
    fig.savefig(rep+"zone"+idZ+"_Eh0")
    

def plot_IH(zone, rep, ts):
    labels = []
    fig = plt.figure()
    Ihc = zone.Ihc.values()
     
    plt.plot(zone.Ihc.keys(), Ihc, color = 'red')
    idZ = zone.getId()
    #labels.append("E0 de la zone "+idZ+" (K="+str(zone.K[0])+")")
   
    #plt.legend(labels, loc = 'best')
    axes = plt.gca()
    axes.set_xlabel('time (day)')
    axes.set_ylabel('number of infected people')
    fig.savefig(rep+"zone"+idZ+"_Ih")


def plot_V(zone, titre):
    
    fig = plt.figure()
    #fig.suptitle(u"effectifs des moustiques selon leurs etats", fontsize=12, fontweight='bold')
    plt.plot(zone.Sv.keys(), zone.Sv.values(), label = 'Sv', color ='blue')
    plt.plot(zone.Ev.keys(), zone.Ev.values(), label = 'Ev', color = 'orange')
    plt.plot(zone.Iv.keys(), zone.Iv.values(), label = 'Iv', color = 'red')
    plt.legend(('Sv', 'Ev', 'Iv'), loc = 'upper right')
    
    axes = plt.gca()
    axes.set_xlabel('temps en jours')
    axes.set_ylabel('Nombre de moustiques dans la zone ')#+str(zone.identifier))
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
#    fig.savefig("demoustication/T/K=0.5/vecteurs_demoustication_t"+titre)
#    plt.close(fig)
    