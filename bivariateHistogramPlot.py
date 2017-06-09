#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:59:13 2017

@author: jfranco1
"""
import plotly as ply
import plotly.graph_objs as go
import numpy as np

t = np.linspace(0,1,2000)
x=data.nthreshold
y=data.ncapacity

trace1 = go.Scatter(
    x=x, y=y, mode='markers', name='points',
    marker=dict(color='rgb(102,0,0)', size=2, opacity=0.4)
)
trace2 = go.Histogram2dcontour(
    x=x, y=y, name='density', ncontours=20,
    colorscale='Hot', reversescale=True, showscale=False
)
trace3 = go.Histogram(
    x=x, name='x density',
    marker=dict(color='rgb(102,0,0)'),
    yaxis='y2'
)
trace4 = go.Histogram(
    y=y, name='y density', marker=dict(color='rgb(102,0,0)'),
    xaxis='x2'
)
dataPlot = [trace1, trace2, trace3, trace4]

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
plot_url = ply.offline.plot(fig, filename='output/histogramOptInstancesBin0')