#! /usr/bin/python
# -*- coding:utf-8 -*-

import re

def parse_goal(g): 
  pattern = re.compile(r"^(?P<square>.*?)(\s+{(?P<logic>.*?)})?\s?$")
  match = pattern.match(g)
  square = match.group("square")
  logic = match.group("logic")

  if logic:
    return (square, logic)
      
  return square

def verify_logic(goals):
  intersections = [
    goals[:5], goals[5:10], goals[10:15], goals[15:20], goals[20:25],
    goals[::5], goals[1::5], goals[2::5], goals[3::5], goals[4::5],
    goals[::6], goals[4::4][:5] 
  ]

  for iset in intersections:
    logic = []
    
    for i in iset:
      if isinstance(i, tuple) and i[1]:
        rules = i[1].split(',')
        for r in rules: 
          logic.append(r) 

    for l in logic:
      if l[0] is "!":
        if l[1:] in logic:
          return []

  return [g[0] if isinstance(g, tuple) else g for g in goals] 
