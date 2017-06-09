#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 16:34:23 2017

@author: juanpf
"""

import random as rd
import pandas as pd
import numpy as np
import copy

#Transforms a list of lists into a list
flatten = lambda l: [item for sublist in l for item in sublist]

def version():
    return (1.0)

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

#Instance categorization and extraction from original files

#Allocates ncapacity and nprofits to bins
#Bins the data received with respect to normalized capacity and profit in nbins bins
#BINS are defined with repect to left edge
def binCapProf(data,nbins):
    dataMZN1=pd.DataFrame(data).copy()
    steps=1/nbins
    #BINS are defined with repect to left edge
    #dataMZN1.ncapacity = pd.cut(dataMZN1.ncapacity,nbins,labels=False)/nbins
    #dataMZN1.nprofit = pd.cut(dataMZN1.nprofit,nbins,labels=False)/nbins
    bins=list(frange(0,1+steps,steps))
    bins[0]=-0.01
    bins[len(bins)-1]=1.01
    #NOBIN
    dataMZN1['ncapacityNoBin']=dataMZN1.ncapacity;
    dataMZN1['nprofitNoBin']=dataMZN1.nprofit;
    #Binned 
    dataMZN1.ncapacity = pd.cut(dataMZN1.ncapacity,bins,labels=False)/nbins
    dataMZN1.nprofit = pd.cut(dataMZN1.nprofit,bins,labels=False)/nbins  
    return dataMZN1


### Add instance type ([1,6]) tp data according to the inputs (Decision Instances)
#nProf: Normalized profit to sample within phase transition
#nCap: Normalized profit to sample within phase transition
#nProfNO: Normalized profit to sample outside the phase transition where there is NO solution
#nProfYes: Normalized profit to sample outside the phase transition where there IS a solution
#quantileLow: Easy instances at (nProf, nCap) are those below the quantileLow
#quantileHigh: Hard instances at (nProf, nCap) are those above the quantileUpper
## OutPut: 1=nProf-easy-NoSolution 2==nProf-easy-Solution 3=nProf-hard-NoSolution
##  3=nProf-hard-Solution 5=nProfNo-NOSolution 6=nProfYES-Solution
def addInstanceType(data,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper):
    dataMZN1=data.copy()
    dataMZN1['instanceType'] = -1
   
    complexity=dataMZN1.propagations[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01)]
    #qUp=complexity.quantile(quantileLow)
    #qDown=complexity.quantile(quantileUpper)
    qUp=complexity.quantile(quantileUpper)
    qDown=complexity.quantile(quantileLow)
    
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
#                          (dataMZN1.propagations<=qDown) & (dataMZN1.solution==0)]=1
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
#                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==1)]=2
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
#                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==0)] =3
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
#                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==1)] =4
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProfNO)<0.01) &
#                    (dataMZN1.solution==0)] =5
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProfYES)<0.01) &
#                    (dataMZN1.solution==1)] =6

    dataMZN1.loc[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
                          (dataMZN1.propagations<=qDown) & (dataMZN1.solution==0),'instanceType']=1
    dataMZN1.loc[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==1),'instanceType']=2
    dataMZN1.loc[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==0),'instanceType'] =3
    dataMZN1.loc[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==1),'instanceType'] =4
    dataMZN1.loc[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProfNO)<0.01) &
                    (dataMZN1.solution==0),'instanceType'] =5
    dataMZN1.loc[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProfYES)<0.01) &
                    (dataMZN1.solution==1),'instanceType'] =6
    return dataMZN1

### Add instance type ([1,6]) tp data according to the inputs (Optimization Instances)
#nProf: Normalized profit to sample within phase transition
#nCap: Normalized profit to sample within phase transition
#nProfNO: Normalized profit to sample outside the phase transition where there is NO solution
#nProfYes: Normalized profit to sample outside the phase transition where there IS a solution
#quantileLow: Easy instances at (nProf, nCap) are those below the quantileLow
#quantileHigh: Hard instances at (nProf, nCap) are those above the quantileUpper
## OutPut: 1=nProf-easy-NoSolution 2==nProf-easy-Solution 3=nProf-hard-NoSolution
##  3=nProf-hard-Solution 5=nProfNo-NOSolution 6=nProfYES-Solution
def addInstanceTypeOpt(data,nCap,nProf,nProfNO,nProfYES,quantileLow,quantileUpper):
    dataMZN1=data.copy()
    dataMZN1['instanceType'] = -1
   
    complexity=dataMZN1.propagations[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01)]
    #qUp=complexity.quantile(quantileLow)
    #qDown=complexity.quantile(quantileUpper)
    qUp=complexity.quantile(quantileUpper)
    qDown=complexity.quantile(quantileLow)
    
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
#                        (dataMZN1.propagations<=qDown) & (dataMZN1.solution==0)]=1
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
                        (dataMZN1.propagations<=qDown)]=2
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
#                    (dataMZN1.propagations>=qUp)& (dataMZN1.solution==0)] =3
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProf)<0.01) & 
                    (dataMZN1.propagations>=qUp)] =4
#    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProfNO)<0.01) &
#                    (dataMZN1.solution==0)] =5
    dataMZN1.instanceType[(np.abs(dataMZN1.ncapacity-nCap)<0.01) & (np.abs(dataMZN1.nprofit-nProfYES)<0.01) ] =6
    return dataMZN1
     

                     

# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Sampling is done with replacement
def sampleInstanceProblems(data,sampleSizePerBin):
    dataMZN1=data.copy()
    sampleProblems=[]
    for j in range(1,7):
        #sampleProblems.extend(dataMZN1.problem[dataMZN1.instanceType==j].sample(n=sampleSizePerBin,replace=True))
        sampleProblems.append(dataMZN1.problem[dataMZN1.instanceType==j].sample(n=sampleSizePerBin,replace=True))
    return sampleProblems


#Extracting Instance informations and exporting into .txt files

#Input: dataframe with the instances and a problem value.
#Return: Profit, Capacity, weights and values AND instanceType
def extractInstance(dataF, problema):
    weights= [[int(y) for y in x.split(',')] for x in dataF.weights[dataF.problem==problema] ]
    values=[ [int(y) for y in x.split(',')] for x in dataF['values'][dataF.problem==problema] ]
    capacity=int(dataF.capacity[dataF.problem==problema])
    profit=int(dataF.threshold[dataF.problem==problema])
    instanceType=int(dataF.instanceType[dataF.problem==problema])
    solution=int(dataF.solution[dataF.problem==problema])
    return (weights[0], values[0], capacity,profit,instanceType, solution)


def extractInstanceOpt(dataF, problema):
    weights= [[int(y) for y in x.split(',')] for x in dataF.weights[dataF.problem==problema] ]
    values=[ [int(y) for y in x.split(',')] for x in dataF['values'][dataF.problem==problema] ]
    capacity=int(dataF.capacity[dataF.problem==problema])
    profit=int(dataF.threshold[dataF.problem==problema])
    instanceType=int(dataF.instanceType[dataF.problem==problema])
    
    itemsOpt= dataF.solution[dataF.problem==problema].values[0]
    cOpt=int(dataF.weightOpt[dataF.problem==problema])
    pOpt=int(dataF.profitOpt[dataF.problem==problema])
    
    return (weights[0], values[0], capacity,profit,instanceType,pOpt,cOpt,itemsOpt)

    
#Input: Profit, Capacity, weights, values and problemID.  
#   The output Folder and the instance number to be maped to the name of the file.)
#Output: Saves the Unity-Task-Compatible ".txt" file for that instance.
def exportInstance(iw,iv,ic,ip,problemID,instanceType, solution ,folderOutput,instanceNumber):
    wS='weights:'+str(iw)
    vS='values:'+str(iv)
    cS='capacity:'+str(ic)
    pS='profit:'+str(ip)
    problemIDS='problemID:'+str(problemID)
    instanceTypeS='instanceType:'+str(instanceType)
    solutionS='solution:'+str(solution)
    string="\n".join([wS, vS, cS, pS,problemIDS,instanceTypeS,solutionS])
    string=string.replace(" ","")
    text_file = open(folderOutput+'i'+str(instanceNumber)+'.txt', "w")
    text_file.write(string)
    text_file.close()
    
    
#Input: Profit, Capacity, weights, values, problemID.... Includes data from Optimization Variant.
#   The output Folder and the instance number to be maped to the name of the file.)
#Output: Saves the Unity-Task-Compatible ".txt" file for that instance.
def exportInstanceOpt(iw,iv,ic,ip,problemID,instanceType,folderOutput,instanceNumber,pOpt,cOpt,itemsOpt):
    wS='weights:'+str(iw)
    vS='values:'+str(iv)
    cS='capacity:'+str(ic)
    problemIDS='problemID:'+str(problemID)
    instanceTypeS='instanceType:'+str(instanceType)
    itemsOptS='solutionItems'+str(itemsOpt)
    cOptS='capacityAtOptimum:'+str(cOpt)
    pOptS='profitAtOptimum:'+str(pOpt)
    string="\n".join([wS, vS, cS,problemIDS,instanceTypeS,pOptS,cOptS,itemsOptS])
    string=string.replace(" ","")
    text_file = open(folderOutput+'i'+str(instanceNumber)+'.txt', "w")
    text_file.write(string)
    text_file.close()
    

##Generates the instance randomization order for bN blocks of tN trials each.   
    
# Generates the randomization within each difficulty; i.e the sampling order for each difficulty level. 
# Input: List of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Output: List of sublist. Each sublist has the randomized indeces of the instances for a difficulty level.
# Assumes that the instance order was saved according to flatten(sampleProblems)
def generateSampleOrderWithin(sampleProblems):
    shufly=[]
    initialIndex=0
    for j in range(0,6):
        temp=range(initialIndex,initialIndex+len(sampleProblems[j]))
        temp=[x for x in temp]
        initialIndex=initialIndex+len(sampleProblems[j])
        rd.shuffle(temp)
        shufly.append(temp)
    return shufly

#Generates de randomization across difficulties for a block
#Input: tN=Number of trials per block
# requires tN to be multiple of 6
#Output: Array with difficulty sequence for a block (labeled as 1,...,6)
def generateBlockDifficultyRand(tN): 
    difficultyOrder=[]
    for k in range(0,int(tN/6)):
        difficultyOrder.extend(range(1,7))
    rd.shuffle(difficultyOrder)
    return(difficultyOrder)


#Chooses the exact instance Order for all trials and blocks based on the difficultyOrder per block and shuffled instances
#instanceOrder starts in 1.
#INPUT: Shufly as returned by generateSampleOrderWithin
def generateInstanceOrder(shufly,tN, bN):
    shuflyTemp=copy.deepcopy(shufly)
    instanceOrder=[]
    for bi in range(0,bN):
        difficultyOrder=generateBlockDifficultyRand(tN);
        for x in difficultyOrder:
            itemToAdd=shuflyTemp[x-1].pop(0)+1
            instanceOrder.extend([itemToAdd])
    return instanceOrder

#Exports:
#The number of trials per block. 
#The number of trials. 
#The number of instance's files.
#The instance order
#INPUT: instanceOrder as returned by generateInstanceOrder, nInstances=number of instances saved to .txt files
def exportTaskInfo(tN,bN,instanceOrder,nInstances,folderOutput):
    tNS='numberOfTrials:'+str(tN)
    bNS='numberOfBlocks:'+str(bN)
    nInstancesS='numberOfInstances:'+str(nInstances)
    instanceOrderS='instanceRandomization:'+str(instanceOrder)        
    string="\n".join([tNS, bNS, nInstancesS, instanceOrderS])
    string=string.replace(" ","")
    text_file = open(folderOutput+'param2.txt', "w")
    text_file.write(string)
    text_file.close()
    
    

    

