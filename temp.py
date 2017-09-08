# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

nITI=7;

np.random.exponential

lower=8
upper=12
scale=1/0.7

expD = stats.truncexpon(b=(upper-lower)/scale, loc=lower, scale=scale)
ITIs = expD.rvs(7)
ITIs=np.round(ITIs,1)








sum(ITIs)
sum(ITIs)/nITI


fig, ax = plt.subplots()
ax.hist(ITIs, normed=True)
plt.show()



# Samples randomly from each instance-type sampleSizePerBin
# Output: list of sublists. Each sublist has sampleSizePerBin size with the instances ID
# Warning: Sampling is done with replacement
sampleProblems=isf.sampleInstanceProblems2(dataOptDec,sampleSizePerBin,possibleTypesOpt)

dataOptDec.columns

dataOptDec.problem[dataOptDec.instanceType==5]

dataOptDec2['diffDecProfandOptProf']=dataOptDec2.nprofitNoBinDec-dataOptDec2.nprofit
           
dataOptDec2.diffDecProfandOptProf[dataOptDec2.instanceType!=-1].hist()

dataOptDec2.diffDecProfandOptProf[dataOptDec2.instanceType==5].hist()

dataOptDec2.diffDecProfandOptProf[dataOptDec2.instanceType==3].hist()

dataOptDec2.nprofitNoBinDec
dataOptDec2.ncapacity


dataOptDec2['diffDecProfandOptProf']


#Falttening sampled problems
sampleProblemsDecF=isf.flatten(sampleProblemsDec)
sampleProblemsOptF=isf.flatten(sampleProblemsOpt)




#Exporting the problems sampled
thefile = open('ISOpt.txt', 'w')
for item in sampleProblemsOptF:
  thefile.write("%s\n" % item)
  #print>>thefile,item
thefile.close()

#getting a histogram of IC algorithmic complexity for slected instaces
a=dataDec.propagations[dataDec.problem.isin(sampleProblemsDecF)]
dataDec.propagations.hist()
a.hist()



           
