#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 17:50:09 2017

@author: khiri
"""

class Etat(object):
    '''
    classe Etat
    -----------
    Contient l'étiquette et le compteur de l'état d'un individu
    
    '''


    def __init__(self, label = 'S', counter = 0):
        '''
        Constructor
        '''
        self.label = label
        self.counter = counter
        
    def getLabel(self):
        return self.label
    
    def getCounter(self):
        return self.counter
    
    def setLabel(self, label):
        self.label = label
        
    def setCounter(self, counter):
        self.counter = counter
        
    def __str__(self):
        return "Etat("+self.label+","+str(self.counter)+")"
        
