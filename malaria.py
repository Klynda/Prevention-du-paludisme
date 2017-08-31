# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 22:00:00 2017

@author: khiri
"""

import numpy
import matplotlib.pyplot as plt
import cPickle as pickle


h = 1. # jours
end_time = 200. # jours
num_steps = int(end_time / h)
times = h * numpy.array(range(num_steps + 1))

Nh = 1000
latencyH = 10.
recoveryH = 9.5*30  # jours
waning_time = 5*365

Nv = 100
latencyV = 11.

K=0.5


betaVHmin = 0.01
betaVHmax = 0.27
betaHVmin = 0.072
betaHVmax = 0.64
betaHVtmin = 0.0072
betaHVtmax = 0.064
sigmaVmin = 0.1
sigmaVmax = 1.0
sigmaHmin = 0.1
sigmaHmax = 50
'''

betaVHmin = 0.022
betaVHmax = 0.022
betaHVmin = 0.24
betaHVmax = 0.48
betaHVtmin = 0.024
betaHVtmax = 0.048
sigmaVmin = 0.33
sigmaVmax = 0.5
sigmaHmin = 4.3
sigmaHmax = 19
'''
'''
mu1Vmin = 0.0010
mu1Vmax = 0.10
mu2Vmin = 1E-6
mu2Vmax = 1E-3
psiVmin = 0.02
psiVmax = 0.27
'''

mu1Vmin = 0.033
mu1Vmax = 0.033
mu2Vmin = 2E-5
mu2Vmax = 4E-5
psiVmin = 0.13
psiVmax = 0.13

probaVH = betaVHmin + K * (betaVHmax - betaVHmin)
betaHVi = betaHVmin + K * (betaHVmax - betaHVmin)
betaHVr = betaHVtmin + K * (betaHVtmax - betaHVtmin)
sigV = sigmaVmin + K * (sigmaVmax - sigmaVmin)
sigH = sigmaHmin + K * (sigmaHmax - sigmaHmin)

mu1V = mu1Vmax - K * (mu1Vmax - mu1Vmin)
mu2V = mu2Vmax - K * (mu2Vmax - mu2Vmin)
psiV = psiVmin + K * (psiVmax - psiVmin)


'''
#valeurs fixée pour dynamique des vecteurs
mu1V = 0.03
mu2V = 0
psiV = 0.03
'''    
'''
bites_per_day_and_mosquito = 0.1 # humans / (day * mosquito)
mosquito_lifetime = 10.0 # days
bite_reduction_by_net = 0.9 # probability
'''
#nombre de contacts (H-M) par unite de temps (jours)
if Nv <= 0.1 :
    b = sigV*Nv
else :
    if Nh <= 0.001 :
        b = sigH*Nh
    else :
        b = (sigV*Nv*sigH*Nh)/(sigV*Nv+sigH*Nh)
    
print "nombre de contacts (H-M) par unite de temps (jours)"
print b


res = {}
def seirs_sei_model(Nv):

    sh = numpy.zeros(num_steps + 1)
    eh = numpy.zeros(num_steps + 1)
    ih = numpy.zeros(num_steps + 1)
    rh = numpy.zeros(num_steps + 1)

    eh[0] = 0.
    ih[0] = 1.
    rh[0] = 0.
    sh[0] = Nh - ih[0] - eh[0] - rh[0]
    
    
    sv = numpy.zeros(num_steps + 1)
    ev = numpy.zeros(num_steps + 1)
    iv = numpy.zeros(num_steps + 1)
    nv = numpy.zeros(num_steps + 1)
    
    nv[0] = Nv

    ev[0] = 0.
    iv[0] = 0.
    sv[0] = Nv - ev[0] - iv[0]
    
    lambdaVH = numpy.zeros(num_steps + 1)
    lambdaHV = numpy.zeros(num_steps + 1)
    

    for step in range(num_steps):
        
        Nv = nv[step]
        if Nv <= 0.001 :
            b = sigV*Nv
        else :
            if Nh <= 0.001 :
                b = sigH*Nh
            else :
                b = (sigV*Nv*sigH*Nh)/(sigV*Nv+sigH*Nh)
                
        print "nombre de contacts (H-M) par unite de temps (jours)"
        print b
        
        if Nv != 0 and Nh != 0:
            lambdaVH[step] = (b/Nh)* probaVH * (iv[step]/Nv)
        else :
            lambdaVH[step] = 0
            
        #lambdaVH[step] = 0.3
        
        sh2eh = h*lambdaVH[step] * sh[step]
        eh2ih = h/latencyH * eh[step]
        ih2rh = h/recoveryH * ih[step]
        rh2sh = h/waning_time * rh[step]
        
        sh[step+1] = sh[step] - sh2eh + rh2sh
        eh[step+1] = eh[step] + sh2eh - eh2ih
        ih[step+1] = ih[step] + eh2ih - ih2rh
        rh[step+1] = rh[step] + ih2rh - rh2sh
        
        ps = sh[step]/Nh
        pe = eh[step]/Nh
        pi = ih[step]/Nh
        pr = rh[step]/Nh
        
        print ps, pe, pi, pr
        
        if Nv != 0 and Nh != 0 :
            lambdaHV[step] = (b/Nv)* ((betaHVi * ih[step] / Nh) + (betaHVr * rh[step] / Nh) )
        else :
            lambdaHV[step] = 0
        #lambdaHV[step] = 0.6
        
        sv2ev = h*lambdaHV[step] * sv[step]
        ev2iv = (h/latencyV) * ev[step]
        
        nv[step] = sv[step]+ev[step]+iv[step]
        fv = mu1V + nv[step]*mu2V
        
        sv[step+1] = psiV*nv[step]+ sv[step] - sv2ev - sv[step]*fv
        ev[step+1] = ev[step] + sv2ev - ev2iv - ev[step]*fv
        iv[step+1] = iv[step] + ev2iv - iv[step]*fv
        '''
        sv[step+1] = sv[step] - sv2ev 
        ev[step+1] = ev[step] + sv2ev - ev2iv 
        iv[step+1] = iv[step] + ev2iv
        '''
        nv[step+1] = sv[step+1]+ev[step+1]+iv[step+1]        
        
    res['V'] = sv, ev, iv , lambdaHV
    res['H'] = sh, eh, ih, rh, lambdaVH
    return res, nv

#sh, eh, ih, rh = seir_sei_model() 
res, nv = seirs_sei_model(Nv) 

print (res['H'][0]) #sh
print "lambdaHV"
print (res['V'][3]) #lambdaVH
print "lambdaVH"
print (res['H'][4])


def plot_H():
    plt.figure()
    plt.plot(times, res['H'][0], label = 'Sh', color='blue')
    plt.plot(times, res['H'][1], label = 'Eh', color='orange')
    plt.plot(times, res['H'][2], label = 'Ih', color='red')
    plt.plot(times, res['H'][3], label = 'Rh', color='green')
    plt.legend(('Sh', 'Eh', 'Ih', 'Rh'), loc = 'upper right')
    #plt.legend(('Eh', 'Ih', 'Rh'), loc = 'upper right')
    
    axes = plt.gca()
    axes.set_xlabel('temps en jours')
    axes.set_ylabel('Nombre de personnes')
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
    plt.ylim([0,Nh])
    
plot_H()

def plot_V():
    
    plt.figure()
    plt.plot(times, res['V'][0], label = 'Sv', color='blue')
    plt.plot(times, res['V'][1], label = 'Ev', color='orange')
    plt.plot(times, res['V'][2], label = 'Iv', color='red')
    plt.legend(('Sv', 'Ev', 'Iv'), loc = 'upper right')
    #plt.legend(('Ev', 'Iv'), loc = 'upper right')
    
    axes = plt.gca()
    axes.set_xlabel('temps en jours')
    axes.set_ylabel('Nombre de moustiques')
    plt.xlim(xmin = 0.)
    plt.ylim(ymin = 0.)
    
plot_V()

print mu1V
print mu2V
print psiV
#plt.plot(range(199), lambdaHV[1:200])
#plt.ylim(ymin = 0.)
#plt.plot(range(199), lambdaHVe[1:200])
#plt.ylim(ymin = 0.)
#
#plt.plot(range(199), lambdaVH[1:200])
#plt.ylim(ymin = 0.)
#plt.plot(range(199), lambdaVHe[1:200])
#plt.ylim(ymin = 0.)
'''
fic = "Validation/modeleChitnis.p"
  
fh = open (fic, 'wb')

pickle.dump(res,fh,pickle.HIGHEST_PROTOCOL)

fh.close()

'''