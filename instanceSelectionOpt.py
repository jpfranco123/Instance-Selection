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

                                                                                                               
                                                                                           
#Before Starting optimization part you must have run intanceSelectionDec and stored the data in dataDec
dataDec=data


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
problemID='-rm-1'
folderInput='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Data/Simulations and Solutions/optimisation/'
folderOut='/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/output/optimization/'

#dataSAT=[];
dataMZN=[];
dataMetrics=[];

#Files to be uploaded with respect to the number of items
cols=[6]#,15,20,25,30]
nCols=len(cols)
 
#Data Upload
for i in cols:
    fileName1=folderInput+str(i)+'/'+'mzn-'+str(i)+problemID+'.csv'
    #fileName2=folder+str(i)+'/'+'sat-'+str(i)+'-analysis.csv'
    fileName3=folderInput+str(i)+'/'+'metrics-'+str(i)+problemID+'.csv'
    
    mzn=pd.read_csv(fileName1,',')
    #sat=pd.read_csv(fileName2,',')
    metrics=pd.read_csv(fileName3,',')
    
    dataMZN.append(mzn)
    #dataSAT.append(sat)
    dataMetrics.append(metrics)
    
#Merges Data from MZN with metrics i  order to add Nprofit and Ncapacity to dataMZN
for i in range(0,nCols):
    dataMZN[i]=pd.merge(dataMZN[i],dataMetrics[i],on='problem')


dataOpt=dataMZN[0]

# Calculates nprofit for the optimization case (i.e. the optimum normalized profit)
dataOpt=isf.calculateOptimum(dataOpt)


# Merges Optimization data and relevant decision columns. 
# Aim: Add instance type from decision Problem to Optimization Problem
# Warning: Here each optimization problem is mapped into many decion problems
data=isf.mergeOptDec(dataDec, dataOpt)


#Keep only those instances where the nProfit of Decision problem (not binned) is the closest to nprofitOpt s.t. nprofitNoBinDec<nprofitOpt
#This give us instances that have solution and are in the phase transition
data=isf.removeRepeatedOptInstances(data)


#Sample Instances
#bN blocks of tN trials 
#requires tN to be multiple of 6
tN=12
bN=3
possibleTypes=[2,4]
nTypes=len(possibleTypes)

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Warning: Sampling is done with replacement
sampleSizePerBin=int(tN*bN/nTypes)

sampleProblems=isf.sampleInstanceProblems(data,sampleSizePerBin,possibleTypes)


#Exports all the instance files in the sampleProblems list
instanceNumber=1
for k in isf.flatten(sampleProblems):
    iw,iv,ic,instanceType,pOpt,cOpt,itemsOpt=isf.extractInstanceOpt(data,k)
    isf.exportInstanceOpt(iw,iv,ic,k,instanceType,folderOut,instanceNumber,pOpt,cOpt,itemsOpt)
    instanceNumber=instanceNumber+1


# Generates the instance randomization order for bN blocks of tN trials 
# This is done for each of the previously exported files

# Generates the randomization within each difficulty; i.e the sampling order for each difficulty level.
shufly=isf.generateSampleOrderWithin(sampleProblems)


#Chooses the exact instance Order for all trials and blocks 
#based on shuffled instances
instanceOrder=isf.generateInstanceOrder(shufly,tN, bN,nTypes)

#Exports 'param2.txt' with the required input for the task
nInstances=len(isf.flatten(sampleProblems))
isf.exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOut)








##################### Mistakes in Decision Files?

#check the match worked
temp=data[['nprofit','nprofitNoBinDec']]
temp['rest']=temp.nprofit-temp.nprofitNoBinDec
temp.describe()


#Check InstanceTypes Here that are 1  and 5 (they are NO solution according to DEC but the proftitQ<Optimum )

problemDec=72-0.27-0.86
Dec:
nc=0.42654
np=0.90625
c=90
p=116
w=38,30,17,24,23,46,33
v=48,4,27,4,41,1,3
sol=0
Opt:
np=0.90625
nc=0.42654
c=90
profitOpt=116


data.instanceType[data.instanceType>0].hist()
data.instanceType[data.instanceType==2].describe()
data.instanceType[data.instanceType==4].describe()

len(data.problem[data.instanceType==5])

prob=data.problemDec[data.instanceType==1].reset_index()
prob=prob.problemDec[0]

decProfit=dataDec[['profit','capacity','weights','values','solution','nprofitNoBin']][dataDec.problem==prob]
decProfit
optProfit=data[['profitOpt','capacity','weights','values','solution','nprofit']][data.problemDec==prob]
optProfit
    
    
data.nprofitNoBinOpt[dataDec.weights==data.weights[0] & data.values==data.values[0] & data.ncapacity==data.ncapacity[0]]

dataDec.instanceType.unique()

dataDec.nprofitNoBin.unique()
dataDec['nprofitNoBin']=dataDec.nprofit


dataDec.weights[dataDec.nprofitNoBin.unique()[0]==dataDec.nprofitNoBin]



