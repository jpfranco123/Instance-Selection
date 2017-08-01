#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:09:57 2017

@author: Pablo Franco

Instance Random Selection
"""

import pandas as pd
#import numpy as np
#import csv
#import random as rd
import importlib
import os

os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')

import instanceSelctionFunctions as isf
importlib.reload(isf)
#import os
#cwd = os.getcwd()

### INPUT ###
problemID='-dm-1'
folderInput='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/decision/'
folderOut='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/decision/'
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
tN=8
bN=7
nTypes=6

#Number of order randomizations (i.e. number of param2.txt files)
nOrderRandomizations=10

### ---- ###

## DATA UPLOAD
dataMZN=isf.importSolvedInstances(nItems,'mzn',folderInput,problemID)
dataSAT=isf.importSolvedInstances(nItems,'sat',folderInput,problemID)


#Allocates ncapacity and nprofits to bins (BINS are defined with repect to left edge (i.e. nCap=0.5 means nCap in [0.5,0.5+binSize] ))
### Add instance type ([1,6]) tp data according to the inputs
#nProf: Normalized profit to sample within phase transition
#nCap: Normalized profit to sample within phase transition
#nProfNO: Normalized profit to sample outside the phase transition where there is NO solution
#nProfYes: Normalized profit to sample outside the phase transition where there IS a solution
#quantileLow: Easy instances at (nProf, nCap) are those below the quantileLow
#quantileHigh: Hard instances at (nProf, nCap) are those above the quantileHigh
## OutPut: 1=nProf-easy-NoSolution 2==nProf-easy-Solution 3=nProf-hard-NoSolution
##  3=nProf-hard-Solution 5=nProfNo-NOSolution 6=nProfYES-Solution

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







#len(dataSM[dataSM.instanceType==3].instanceType)
#
#dataSM[dataSM.instanceType==4].problem
#dataSM['itemsID']= [ x.split('-')[0] for x in dataSM.problem ]
#
#len(dataSM['itemsID'][dataSM.instanceType==6].unique())
#len(dataSM['itemsID'][dataSM.instanceType==2])


######################
## Taking only MZN solver output for instance Type categorization
#data=dataMZN[0]
#data=isf.binCapProf(data,nbins)
#data=isf.addInstanceType(data,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper,'propagations')

######################3



## SAMPLING of Instances

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Sampling is done withOUT replacement
#sampleSizePerBin=int(tN*bN/nTypes)
sizePerBin=int(tN*bN/(nTypes+2))
sampleSizePerBin=[sizePerBin,sizePerBin,sizePerBin,sizePerBin,2*sizePerBin,2*sizePerBin]
possibleTypes=range(1,nTypes+1)
sampleProblems=isf.sampleInstanceProblems3(dataDec,sampleSizePerBin,possibleTypes)

#Exports all the instance files in the sampleProblems list
instanceNumber=1
for k in isf.flatten(sampleProblems):
    iw,iv,ic,ip,instanceType,solution=isf.extractInstance(dataDec,k)
    isf.exportInstance(iw,iv,ic,ip,k,instanceType,solution,folderOut,instanceNumber)
    instanceNumber=instanceNumber+1

## INSTANCE ORDER GENERATION and param2.txt export

# Generates the instance randomization order for bN blocks of tN trials for nTypes instance types
nInstances=tN*bN
for i in range(0,nOrderRandomizations):
    instanceOrder=isf.generateInstanceOrder(tN, bN,nTypes)
    
    #Exports 'param2.txt' with the required input for the task
    
    isf.exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOut,i)
    

#Generates Intertrial intervals and exports it to paramMRI.txt
isf.exportITIs(tN,bN,folderOut)






    
    
    
    
    
    
    
    
######################
# SAT and MZN instanceType Comparison #

dataS=dataSAT[0]
dataS=isf.binCapProf(dataS,nbins)
dataS=isf.addInstanceType(dataS,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper,'decisions')

#Subset the data frame and change the name of dataInstance
dataM=dataMZN[0]
dataM=isf.binCapProf(dataM,nbins)
dataM=isf.addInstanceType(dataM,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper,'propagations')


dataM['instanceTypeMZN']=dataM.instanceType
dataM=dataM[['instanceTypeMZN','problem','propagations']]

#change name of dataInstance
dataS['instanceTypeSAT']=dataS.instanceType
dataS=dataS[['instanceTypeSAT','problem','decisions']]

dataSM=pd.merge(dataS,dataM,on='problem')
dataSMsub=dataSM[dataSM.instanceTypeMZN.isin([1,2,3,4])]


sum(dataSMsub.instanceTypeSAT!=dataSMsub.instanceTypeMZN)
dataSMsub.plot.scatter(x='instanceTypeMZN',y='instanceTypeSAT')


dataSMsub.instanceTypeSAT[dataSMsub.instanceTypeSAT!=dataSMsub.instanceTypeMZN].plot.hist()

dataSM.instanceTypeMZN[dataSM.instanceTypeSAT!=dataSM.instanceTypeMZN].plot.hist()

#If we take intersection of MZN and SAT we still get enough instances
dataSMsub.instanceTypeMZN[dataSMsub.instanceTypeSAT==dataSMsub.instanceTypeMZN].plot.hist()

#This is an interesting plot 1-MZN->1-SAT and 4-MZN->4-SAT
dataSM.plot.scatter(x='instanceTypeMZN',y='instanceTypeSAT')
len(dataSM.instanceTypeMZN[dataSM.instanceTypeMZN==1])
len(dataSM.instanceTypeMZN[dataSM.instanceTypeMZN==3])
len(dataSM.instanceTypeSAT[dataSM.instanceTypeSAT==1])
len(dataSM.instanceTypeSAT[dataSM.instanceTypeSAT==3])

len(dataS.instanceTypeSAT[dataS.instanceTypeSAT==2])

len(dataM.instanceTypeMZN[dataM.instanceTypeMZN==4])


dataM.propagations[(np.abs(dataM.ncapacity-nCap)<0.01) & (np.abs(dataM.nprofit-nProf)<0.01) &
                         (dataM.solution==0)].plot.hist()

mprop=dataM.propagations[(np.abs(dataM.ncapacity-nCap)<0.01) & (np.abs(dataM.nprofit-nProf)<0.01) &
                         (dataM.solution==1)]
mprop.describe()


dataS.decisions[(np.abs(dataS.ncapacity-nCap)<0.01) & (np.abs(dataS.nprofit-nProf)<0.01) &
                         (dataS.solution==0)].plot.hist()

sdec=dataS.decisions[(np.abs(dataS.ncapacity-nCap)<0.01) & (np.abs(dataS.nprofit-nProf)<0.01) &
                         (dataS.solution==1)]
sdec.describe()

#66 check qUp=complexity.quantile(quantileUpper) works as expected
qUp=sdec.quantile(0.2)
len(sdec[sdec<=qUp])

qUp=mprop.quantile(0.8)
len(mprop[mprop>=qUp])


####################
    
    
