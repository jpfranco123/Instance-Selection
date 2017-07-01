#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 19:12:14 2017

@author: jfranco1
"""

#HAVE TO CHANHGE THE DIRECTORY
import libstats

def xrange(*arg):
    if len(arg) ==1 :
          return range(arg[0])
    elif len(arg) ==2:
          return range(arg[0],arg[1])
    elif len(arg) ==3:
          return range(arg[0],arg[1],arg[2])
      
xrange=range


xrange(10,20)

data = data.reset_index(drop=True)
v=data.valuesArr[0]
w=data.weightsArr[0]
c=data.capacity[0]
solution_items=data.solution[0]

instance = Instance(v, w, c, solution_items)

instance.solution()
get_sahni_k(instance)