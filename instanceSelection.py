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
import random as rd
import importlib
import os



os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')

import instanceSelctionFunctions as isf
importlib.reload(isf)
#import os
#cwd = os.getcwd()

#jfranco1
folderInput='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Simulations and Solutions/'
folderOut='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/'

#dataSAT=[];
dataMZN=[];
dataMetrics=[];

#Files to be uploaded with respect to the number of items
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
    
#Merges Data from MZN with metrics i  order to add Nprofit and Ncapacity to dataMZN
for i in range(0,nCols):
    dataMZN[i]=pd.merge(dataMZN[i],dataMetrics[i],on='problem')


data=dataMZN[0]

#number of bins to allocate the data
nbins=20
#Allocates ncapacity and nprofits to bins
#BINS are defined with repect to left edge (i.e. nCap=0.5 means nCap in [0.5,0.5+binSize] )
data=isf.binCapProf(data,nbins)

### Add instance type ([1,6]) tp data according to the inputs
#nProf: Normalized profit to sample within phase transition
#nCap: Normalized profit to sample within phase transition
#nProfNO: Normalized profit to sample outside the phase transition where there is NO solution
#nProfYes: Normalized profit to sample outside the phase transition where there IS a solution
#quantileLow: Easy instances at (nProf, nCap) are those below the quantileLow
#quantileHigh: Hard instances at (nProf, nCap) are those above the quantileHigh
## OutPut: 1=nProf-easy-NoSolution 2==nProf-easy-Solution 3=nProf-hard-NoSolution
##  3=nProf-hard-Solution 5=nProfNo-NOSolution 6=nProfYES-Solution
nProf=0.55
quantileLow=0.4
quantileUpper=0.6
nProfNO=0.9
nProfYES=0.2
nCap=0.4
data=isf.addInstanceType(data,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper)

#bN blocks of tN trials 
#requires tN to be multiple of 6
tN=12
bN=3

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Warning: Sampling is done with replacement
sampleSizePerBin=int(tN*bN/6)
sampleProblems=isf.sampleInstanceProblems(data,sampleSizePerBin)



#Exports all the instance files in the sampleProblems list
instanceNumber=1
for k in isf.flatten(sampleProblems):
    iw,iv,ic,ip,instanceType=isf.extractInstance(data,k)
    isf.exportInstance(iw,iv,ic,ip,k,instanceType,folderOut,instanceNumber)
    instanceNumber=instanceNumber+1


# Generates the instance randomization order for bN blocks of tN trials 
# This is done for each of the previously exported files

# Generates the randomization within each difficulty; i.e the sampling order for each difficulty level.
shufly=isf.generateSampleOrderWithin(sampleProblems)


#Chooses the exact instance Order for all trials and blocks 
#based on shuffled instances
instanceOrder=isf.generateInstanceOrder(shufly,tN, bN)

#Exports 'param2.txt' with the required input for the task
nInstances=len(isf.flatten(sampleProblems))
isf.exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOut)



  







