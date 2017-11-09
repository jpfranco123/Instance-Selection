# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#KS Decision Instance for Karlo (IC x 3 project)

import pandas as pd
import importlib
import os

os.chdir('/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')

import instanceSelctionFunctions as isf
importlib.reload(isf)

folderOutDec='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/ICx3/Output/Dec/'

folderInputDec1='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/ICx3/Input/'

subSample=pd.read_csv(folderInputDec+'ISDec.txt',',')

folderInputDec2='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/decision/'

#number of bins to allocate ncapacity and nprofits to bins
nbins=20

#Normalized capacity from which to sample instances
nCap=0.4

#Normalized profit from which to sample IN-Phase-Transition instanes
nProf=0.6

#Normalized profit from which to sample OUT-OF-Phase-Transition instanes
nProfNO=0.85
nProfYES=0.35

#How to categorize easy/hard IN-Phase-Transition
quantileLow=0.5
quantileUpper=0.5

#bN blocks of tN trials
#requires tN to be multiple of nTypes
tNDec=24
bNDec=1
nTypesDec=6

problemIDDec='-dm-1'

nOrderRandomizations=10


## DATA UPLOAD
dataMZN=isf.importSolvedInstances(nItems,'mzn',folderInputDec2,problemIDDec)

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
## Taking instance categorized according to MZN

dataM=dataMZN[0]
dataM=isf.binCapProf(dataM,nbins)
dataM=isf.addInstanceType(dataM,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper,'propagations')


dataDec=dataM


## SAMPLING of Instances

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Sampling is done withOUT replacement
sizePerBin=int(tNDec*bNDec/(nTypesDec+2))
#Total number (Including all blocks) instances per Type
sampleSizePerBin=[sizePerBin,sizePerBin,sizePerBin,sizePerBin,2*sizePerBin,2*sizePerBin] 
possibleTypesDec=range(1,nTypesDec+1)
sampleProblems=isf.sampleInstanceProblems3(dataDec,sampleSizePerBin,possibleTypesDec)

#Exports all the instance files in the sampleProblems list
instanceNumber=1
for k in isf.flatten(sampleProblems):
    iw,iv,ic,ip,instanceType,solution=isf.extractInstance(dataDec,k)
    isf.exportInstance(iw,iv,ic,ip,k,instanceType,solution,folderOutDec,instanceNumber)
    instanceNumber=instanceNumber+1


#### Instance Order Randomisation

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
sizePerBin=int(tNDec*bNDec/(nTypesDec+2))
#Total number (Including all blocks) instances per Type
sampleSizePerBin=[sizePerBin,sizePerBin,sizePerBin,sizePerBin,2*sizePerBin,2*sizePerBin] 

nInstances=tNDec*bNDec
for i in range(0,nOrderRandomizations):
    instanceOrder=isf.generateInstanceOrder(tNDec, bNDec,sampleSizePerBin)
    isf.exportTaskInfo(tNDec,bNDec,instanceOrder,nInstances,folderOutDec,i) #Exports 'param2.txt' with the required input for the task

