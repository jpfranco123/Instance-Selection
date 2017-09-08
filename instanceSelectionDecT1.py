#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:37:28 2017
@author: juanpf
"""

import pandas as pd
import random as rd
import importlib
import os

os.chdir('/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')

import instanceSelctionFunctions as isf
importlib.reload(isf)

### INPUT ###
problemID='-dm-1'
folderInput='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/decision/'
folderOut='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/decision/'
#Files to be uploaded with respect to the number of items
nItems=[6]#,15,20,25,30]

#number of bins to allocate ncapacity and nprofits to bins
nbins=20

#Normalized capacity from which to sample instances
nCap=0.6

#Normalized profit from which to sample IN-Phase-Transition instanes
nProf=0.75

#Normalized profit from which to sample OUT-OF-Phase-Transition instanes
nProfNO=0.9
nProfYES=0.6

#How to categorize easy/hard IN-Phase-Transition
quantileLow=0.2
quantileUpper=0.8

#bN blocks of tN trials
#requires tN to be multiple of nTypes
tN=21
bN=3
nTypes=7

#Number of order randomizations (i.e. number of param2.txt files)
nOrderRandomizations=10

### ---- ###

## DATA UPLOAD
dataMZN=isf.importSolvedInstances(nItems,'mzn',folderInput,problemID)
dataSAT=isf.importSolvedInstances(nItems,'sat',folderInput,problemID)

####################
## Taking only the intersection of instances categorized equally with MZN and SAT

dataM=dataMZN[0]
dataM=isf.binCapProf(dataM,nbins)
dataM=isf.addInstanceType(dataM,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper,'propagations')

dataS=dataSAT[0]
dataS=isf.binCapProf(dataS,nbins)
dataS=isf.addInstanceType(dataS,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper,'decisions')

dataS['instanceTypeSAT']=dataS.instanceType
dataS=dataS[['instanceTypeSAT','problem','decisions']]

dataSM=pd.merge(dataS,dataM,on='problem')
dataSM=dataSM[dataSM.instanceTypeSAT==dataSM.instanceType]

dataSM[dataSM.instanceType!=-1].instanceType.hist()
dataDec=dataSM


## SAMPLING of Instances

sampleSizePerBin=int(tN*bN/nTypes)
possibleTypes=list(range(1,nTypes))
possibleTypes.append(-1)
sampleProblems=isf.sampleInstanceProblems2(dataDec,sampleSizePerBin,possibleTypes)

#Randomizes the ratio problems (control trials) with respect to them having or not solution
#66
if (sampleSizePerBin !% 2 ):
    lengthRand=sampleSizePerBin+1
else:
    lengthRand=sampleSizePerBin

ratioRandomization=isf.generateBlockDifficultyRand(lengthRand,2)
ratioRandomization = [(x-1) for x in ratioRandomization]

#Exports all the instance files in the sampleProblems list
instanceNumber=1
ratioIndex=0
for k in isf.flatten(sampleProblems):
    iw,iv,ic,ip,instanceType,solution=isf.extractInstance(dataDec,k)
    if(instanceType != -1):
        ratioQ=-1
    else:
        solution=ratioRandomization[ratioIndex]
        ratioIndex=ratioIndex+1
        indeces=range(0,len(iw))
        c=[float(iv[x])/float(iw[x]) for x in indeces]
        if(solution==0):
            ratioQ=int(max(c)*2)/2 + 1
        else:
            ratioQ=int(max(c)*2)/2 - 0.5
            if(ratioQ<=0):
                ratioQ=(int(max(c)*2)/2)*0.5
    isf.exportInstanceDecT1(iw,iv,ic,ip,k,instanceType,solution,ratioQ,folderOut,instanceNumber)
    instanceNumber=instanceNumber+1

## INSTANCE ORDER GENERATION and param2.txt export

# Generates the instance randomization order for bN blocks of tN trials for nTypes instance types
nInstances=tN*bN
for i in range(0,nOrderRandomizations):
    instanceOrder=isf.generateInstanceOrder(tN, bN,nTypes)
    
    #Exports 'param2.txt' with the required input for the task
    isf.exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOut,i)
    