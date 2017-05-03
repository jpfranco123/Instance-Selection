#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:09:57 2017

@author: Pablo Franco

Instance Random Selection 
"""

import pandas as pd
import numpy as np
import csv
#import decimal
import random as rd

import instanceSelctionFunctions

#import os
#cwd = os.getcwd()

#jfranco1
folderInput='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Simulations and Solutions/'
folderOut='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Phase Transitions/Instance Selection/output/'

dataSAT=[];
dataMZN=[];
dataMetrics=[];

cols=[7]#,15,20,25,30]
nCols=len(cols)

 
#Data Upload
for i in cols:
    fileName1=folderInput+str(i)+'/'+'mzn-'+str(i)+'-analysis.csv'
    #fileName2=folder+str(i)+'/'+'sat-'+str(i)+'-analysis.csv'
    fileName3=folderInput+str(i)+'/'+'metrics-'+str(i)+'-analysis.csv'
    
    mzn=pd.read_csv(fileName1,',')
    #sat=pd.read_csv(fileName2,',')
    metrics=pd.read_csv(fileName3,',')
    
    dataMZN.append(mzn)
    #dataSAT.append(sat)
    dataMetrics.append(metrics)
    
    #Add Nprofit and Ncapacity to dataMZN
for i in range(0,nCols):
    dataMZN[i]=pd.merge(dataMZN[i],dataMetrics[i],on='problem')

#Allocates ncapacity and nprofits to bins
nbins=20
for i in range(0,nCols):
    #bins=frange(-0.1,1.11,0.05)
    dataMZN1=pd.DataFrame(dataMZN[i]).copy()
    #dataMZN1=pd.DataFrame(dataMZN).copy()
    #BINS are defined with repect to left edge
    dataMZN1.ncapacity = pd.cut(dataMZN1.ncapacity,nbins,labels=False)/nbins
    #dataMZN1.ncapacity.round(1)
    dataMZN1.nthreshold = pd.cut(dataMZN1.nthreshold,nbins,labels=False)/nbins
    
    dataMZN1['instanceType'] = -1
    nProf=0.55
    nProfNO=0.9
    nProfYES=0.2
    nCap=0.4
    complexity=dataMZN1.propagations[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01)]
    qUp=complexity.quantile(0.4)
    qDown=complexity.quantile(0.6)
    
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==0)]=1
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==1)]=2
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==0)] =3
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==1)] =4
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProfNO)<0.01) &
                    (dataMZN1.solution==0)] =5
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProfYES)<0.01) &
                    (dataMZN1.solution==1)] =6
                          
    sampleSizePerBin=10
    sampleProblems=[]
    for j in range(1,7):
        #sampleProblems.extend(dataMZN1.problem[dataMZN1.instanceType==j].sample(n=sampleSizePerBin,replace=True))
        sampleProblems.append(dataMZN1.problem[dataMZN1.instanceType==j].sample(n=sampleSizePerBin,replace=True))

    



    



#Exports all the instance files in the sampleProblems array
instanceNumber=1
for k in flatten(sampleProblems):
    iw,iv,ic,ip=extractInstance(dataMZN1,k)
    exportInstance(iw,iv,ic,ip,folderOut,instanceNumber)
    instanceNumber=instanceNumber+1



#Generates the instance randomization order for bN blocks of tN trials each for the previously exported files
tN=12
bN=3

shufly=generateSampleOrderWithin(sampleProblems)

#requires tN to be multiple of 6
difficultyOrder=generateBlockDifficultyRand(tN)

instanceOrder=generateInstanceOrder(difficultyOrder, shufly, bN)

nInstances=len(flatten(sampleProblems))
exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOutput)






def binCapProf(data,nbins)
    dataMZN1=pd.DataFrame(data).copy()
    #BINS are defined with repect to left edge
    dataMZN1.ncapacity = pd.cut(dataMZN1.ncapacity,nbins,labels=False)/nbins
    dataMZN1.nthreshold = pd.cut(dataMZN1.nthreshold,nbins,labels=False)/nbins
    return dataMZN1
    dataMZN1['instanceType'] = -1
    nProf=0.55
    nProfNO=0.9
    nProfYES=0.2
    nCap=0.4
    complexity=dataMZN1.propagations[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01)]
    qUp=complexity.quantile(0.4)
    qDown=complexity.quantile(0.6)
    
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==0)]=1
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==1)]=2
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==0)] =3
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==1)] =4
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProfNO)<0.01) &
                    (dataMZN1.solution==0)] =5
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nthreshold-nProfYES)<0.01) &
                    (dataMZN1.solution==1)] =6
                          
    sampleSizePerBin=10
    sampleProblems=[]
    for j in range(1,7):
        #sampleProblems.extend(dataMZN1.problem[dataMZN1.instanceType==j].sample(n=sampleSizePerBin,replace=True))
        sampleProblems.append(dataMZN1.problem[dataMZN1.instanceType==j].sample(n=sampleSizePerBin,replace=True))

    


















        
#    shufly=[]
#    for j in range(0,6):
#        temp=range(0+sampleSizePerBin*j,sampleSizePerBin*(j+1))
#        rd.shuffle(temp)
#        shufly.append(temp)
  







