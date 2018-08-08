#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:00:15 2017

@author: Pablo Franco (jpfranco123@gmail.com)

Instance order Randomisation. To be used only if additional order randomisations are neededself.

@Dependencies:
instanceSelctionFunctions.py

@Output:
1.param2.txt instance information files with different order ransomisations:
numberOfTrials:9
numberOfBlocks:2
numberOfInstances:18
instanceRandomization:[10,15,11,1,14,18,4,5,12,3,7,13,6,17,8,16,2,9]

"""


#KS Decision Instance, Instance order generation (param2.txt)

import pandas as pd
import importlib
import os

#Project folder
folder = '/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Research/Complexity Project/'
os.chdir( folder +'KS-IC/Instance Selection/')

import instanceSelctionFunctions as isf
importlib.reload(isf)

nOrderRandomizationsMin=1#0#1
nOrderRandomizations=30

#Decision

folderOutDec= folder + 'KS-IC/Data/Simulations/instanceSelectionOutput/decision/'
tNDec=8
bNDec=7


nTypesDec=6

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
sizePerBin=int(tNDec*bNDec/(nTypesDec+2))
#Total number (Including all blocks) instances per Type
sampleSizePerBin=[sizePerBin,sizePerBin,sizePerBin,sizePerBin,2*sizePerBin,2*sizePerBin]

nInstances=tNDec*bNDec
for i in range(nOrderRandomizationsMin,nOrderRandomizations):
    instanceOrder=isf.generateInstanceOrder(tNDec, bNDec,sampleSizePerBin)
    isf.exportTaskInfo(tNDec,bNDec,instanceOrder,nInstances,folderOutDec,i) #Exports 'param2.txt' with the required input for the task

#Optimisation
folderOutOpt= folder + 'KS-IC/Data/Simulations/instanceSelectionOutput/optimisation/'
#folderOutOpt='/Users/juanpf/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/optimization/'

#bN blocks of tN trials
#requires tN to be multiple of the number of instances types there are
tNOpt=9
bNOpt=2
possibleTypesOpt=[1,3,5]

nTypesOpt=len(possibleTypesOpt)
sizePerBin=int(tNOpt*bNOpt/(nTypesOpt))
sampleSizePerBin=[sizePerBin,sizePerBin,sizePerBin]
#sampleSizePerBin=int(tNOpt*bNOpt/nTypesOpt)

nInstances=tNOpt*bNOpt
for i in range(nOrderRandomizationsMin,nOrderRandomizations):
    instanceOrder=isf.generateInstanceOrder(tNOpt, bNOpt,sampleSizePerBin)
    isf.exportTaskInfo(tNOpt,bNOpt,instanceOrder,nInstances,folderOutOpt,i)#Exports 'param2.txt' with the required input for the task
