#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:49:56 2017

@author: jfranco1
"""
import os
import plotly as ply
import plotly.graph_objs as go
import numpy as np
import pandas as pd


os.chdir('/Users/jfranco1/Google Drive/Melbourne/UNIMELB/Complexity Project/Code/Instance Selection/')



## From Instance Selection Dec
fileName='scatterInstanceType'
nprofit=dataDec.nprofitNoBin
ncapacity=dataDec.ncapacityNoBin
instanceType=dataDec.instanceType

# Plot instances on normalized capacity and normalized profit grid, deifferentiating by instance type
plotInstancesByType(ncapacity,nprofit,instanceType,fileName)


##From Phase Transition:
#Adjusting the ncapacity and nprofit bins to be  represented by the center of the bin instead of the left edge for potting
meanPlot=meanMZN[1].copy()
meanPlot.solution=np.abs(meanPlot.solution-0.5)
meanPlot.ncapacityBin=meanPlot.ncapacityBin + 1/(nbins*2)
meanPlot.nprofitBin=meanPlot.nprofitBin + 1/(nbins*2)

nprofitPT=meanPlot.nprofitBin
ncapacityPT=meanPlot.ncapacityBin
probSolutionPT=meanPlot.solution

##From Instance Selection Opt:
nprofit=data.nProfitOpt
ncapacity=data.ncapacity

# Scatter instanes in NP and ND grid
fileName='scatterInstanceType'
plotInstancesInNpNcGrid(nprofit,ncapacity,fileName)

# Plot instances And Phase Transition
fileName='instancesAndPhaseTransition'
plotInstancesAndPhaseT(nprofit,ncapacity,nprofitPT,ncapacityPT,probSolutionPT,fileName)




# Input: 3 vectors with nproft, ncapacity, instanceType. Alose the File Name
# Plot instances on normalized capacity and normalized profit grid, deifferentiating by instance type
# Plots only categorized instances; i.e. not "-1" (If we look at too many data points: it just looks like a square)
def plotInstancesByType(ncapacity,nprofit,instanceType,fileName):
    fig = {
    'data': [
        {
            'x': nprofit[instanceType==iT],
            'y': ncapacity[instanceType==iT],
            'name': iT, 'mode': 'markers',
        } for iT in [1,2,3,4,5,6]
    ],
    'layout': {
        'xaxis': {'title': 'Normalized Profit'},
        'yaxis': {'title': "Normalized Capacity"}
    }
    }

    ply.offline.plot(fig, filename='output/'+ fileName +'.html')
    
#    # Plot All Instance Types (Too many data points: Just looks like a square)
#    groups = dataDec.groupby('instanceType')
#    fig, ax = plt.subplots()
#    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
#    for name, group in groups:
#        ax.plot(group.ncapacityNoBin, group.nprofitNoBin, marker='.', linestyle='', ms=1, label=name)
#    ax.legend()
#    plt.show() 


#Plots a heat map of where the instances lie in terms of ncapacity and nprofit
def plotInstancesInNpNcGrid(nprofit,ncapacity,fileName):  
    x=nprofit
    y=ncapacity
    
    trace1 = go.Histogram2dcontour(
        x=x, y=y, name='density', ncontours=20,
        colorscale='Hot', reversescale=True, showscale=False
    )
    trace2 = go.Histogram(
        x=x, name='x density',
        marker=dict(color='rgb(102,0,0)'),
        yaxis='y2'
    )
    trace3 = go.Histogram(
        y=y, name='y density', marker=dict(color='rgb(102,0,0)'),
        xaxis='x2'
    )
    dataPlot = [trace1, trace2, trace3]
    
    layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=600,
        height=550,
        xaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False,
            title='nProfit'
        ),
        yaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False,
            title='nCapacity'
        ),
        margin=dict(
            t=50
        ),
        hovermode='closest',
        bargap=0,
        xaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        ),
        yaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        )
    )
    
    fig = go.Figure(data=dataPlot, layout=layout)
    ply.offline.plot(fig, filename='output/'+fileName+'.html')
    
    


# Plot instances on normalized capacity and normalized profit grid together with phase Transition.
# Input: 
# nprofit, ncapacity: Instance sampling Info. 
# nprofitPT,ncapacityPT,probSolutionPT: Phase Transition Info, i.e. binned nprofit and ncapacity with its correponding probability of there being a solution.
def plotInstancesAndPhaseT(nprofit,ncapacity,nprofitPT,ncapacityPT,probSolutionPT,fileName):  
    x=nprofit
    y=ncapacity
    
    x1=nprofitPT
    y1=ncapacityPT
    z1=probSolutionPT
    
    trace1 = go.Scatter(
    x=x, y=y, mode='markers', name='points',
    marker=dict(color='rgb(102,0,0)', size=2, opacity=0.4)
    )
    trace2 = go.Histogram(
        x=x, name='x density',
        marker=dict(color='rgb(102,0,0)'),
        yaxis='y2'
    )
    trace3 = go.Histogram(
        y=y, name='y density', marker=dict(color='rgb(102,0,0)'),
        xaxis='x2'
    )
    trace4 = go.Heatmap(
        x=x1, y=y1,z=z1, name='phaseT',
        colorscale='Greens', reversescale=False, showscale=False
    )

    dataPlot = [trace1, trace2, trace3,trace4]
    
    layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=600,
        height=550,
        xaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False,
            title='nProfit'
        ),
        yaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False,
            title='nCapacity'
        ),
        margin=dict(
            t=50
        ),
        hovermode='closest',
        bargap=0,
        xaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        ),
        yaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        )
    )
    
    fig = go.Figure(data=dataPlot, layout=layout)
    ply.offline.plot(fig, filename='output/'+fileName+'.html')
    