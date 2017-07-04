#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 11:09:57 2017

@author: Pablo Franco

Instance Random Selection 
"""

#66 TODO: Homologar (npcapacity and ncapacityBin) and (nProfit and nprofitBin) 
#en el momento se diferencia ncapacity de ncapacityNoBin (same for nprofit) para Decision problem, 
# pero para Optimization ncapacity y nprofit no son Binned
#Entonces ncapacity cuando se hace el merge de las dataframes es NoBin, pero se llama ncapacity...
#Make standard No BIn: i.e. ncapacity and nprofit are not binned . And create for decision problem ncapacityBin(nprof..): and change all dependendencies

#import pandas as pd
#import numpy as np
#import csv
#import random as rd
import importlib
import os
os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')
import instanceSelctionFunctions as isf
importlib.reload(isf)                                                                                                       
                                                                                           
#IMPORTANT! Before Starting optimization part you must have run intanceSelectionDec and stored the data in dataDec

### INPUT ###
problemID='-rm-1'
folderInput='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/optimisation/'
folderOut='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/optimization/'

#Files to be uploaded with respect to the number of items
nItems=[6]#,15,20,25,30]

#bN blocks of tN trials 
#requires tN to be multiple of the number of instances types there are
tN=9
bN=2
#An array with possible types
possibleTypes=[2,4,6]

#Number of order randomizations (i.e. number of param2.txt files)
nOrderRandomizations=10

### ---- ###   
    
### Data Upload
dataMZN=isf.importSolvedInstances(nItems,'mzn',folderInput,problemID)
dataSAT=isf.importSolvedInstances(nItems,'sat',folderInput,problemID)


### Instance Type Attachment
dataOpt=dataMZN[0]

# Calculates nprofit for the optimization case (i.e. the optimum normalized profit)
dataOpt=isf.calculateOptimum(dataOpt)

# Merges Optimization data and relevant decision columns. 
# Aim: Add instance type from decision Problem to Optimization Problem
# Warning: Here each optimization problem is mapped into many decion problems
dataOptDec=isf.mergeOptDec(dataDec, dataOpt)


#Keep only those instances where the nProfit of Decision problem (not binned) is the closest to nprofitOpt s.t. nprofitNoBinDec<nprofitOpt
#This give us instances that have solution and are in the phase transition
dataOptDec=isf.removeRepeatedOptInstances(dataOptDec)


### Sample Instances

nTypes=len(possibleTypes)
sampleSizePerBin=int(tN*bN/nTypes)

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Warning: Sampling is done with replacement
sampleProblems=isf.sampleInstanceProblems(dataOptDec,sampleSizePerBin,possibleTypes)

#Exports all the instance files in the sampleProblems list
instanceNumber=1
for k in isf.flatten(sampleProblems):
    iw,iv,ic,instanceType,pOpt,cOpt,itemsOpt=isf.extractInstanceOpt(dataOptDec,k)
    isf.exportInstanceOpt(iw,iv,ic,k,instanceType,folderOut,instanceNumber,pOpt,cOpt,itemsOpt)
    instanceNumber=instanceNumber+1

## INSTANCE ORDER GENERATION and param2.txt export

# Generates the instance randomization order for bN blocks of tN trials for nTypes instance types
nInstances=tN*bN
for i in range(0,nOrderRandomizations):
    instanceOrder=isf.generateInstanceOrder(tN, bN,nTypes)
    
    #Exports 'param2.txt' with the required input for the task
    isf.exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOut,i)
    


