#! /usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, requests

from logic import parse_goal, verify_logic
from config import *

from flask import Flask
from random import shuffle, randint
from pathlib import Path
from functools import wraps
from flask import render_template, flash, redirect, request, Response, jsonify

app = Flask(__name__)

@app.route('/ds1bingo/lockout')
@app.route('/ds1bingo/lockout/')
@app.route('/ds1bingo/team')
@app.route('/ds1bingo/team/')
def route_landing():
  return redirect('http://arcandpoint.com/ds1bingo',
    code=302
  )

@app.route('/ds1bingo')
@app.route('/ds1bingo/')
@app.route('/ds1bingo/<seed>')
def route_bingo(seed=None):  
  try:
    seed = int(seed.strip())
  except ValueError:
    print('Someone tried this seed: {0}'.format(seed))
  except AttributeError:
    print('Seed empty, generating new seed...')

  if isinstance(seed, int) and len(str(seed)) == 7:
    seed_file = Path('{0}/seeds/{1}'.format(ROOT_PATH, str(seed)))
    bingo_goalset = []
    goals = []

    if seed_file.is_file():
      with open(seed_file) as f:
        lines = f.read().splitlines()
      for l in lines:
        bingo_goalset.append(l)
    else:
      with open('{0}/goals.static'.format(ROOT_PATH)) as f:
        lines = f.read().splitlines()
      for l in lines:
        if l.strip() and l[0] not in ["#", "@"]:
          goals.append(parse_goal(l))
      
      while not bingo_goalset: 
      	shuffle(goals)
      	bingo_goalset = verify_logic(goals[:25])

      with open('{0}/seeds/{1}'.format(ROOT_PATH, str(seed)), 'w') as f:
        for g in bingo_goalset:
          f.write('{0}\n'.format(g))

    return render_template('base.html',
      name='page-base',
      goals=bingo_goalset,
      seed=seed
    )
  else:
    seed = randint(1000000, 9999999)
    return redirect('http://arcandpoint.com/ds1bingo/{0}'.format(seed),
      code=302
    )

app.route('/ds1bingo/lockout/<seed>')
def route_lockout(seed=None):
  return redirect('http://arcandpoint.com/ds1bingo',
    code=302
  )

app.route('/ds1bingo/team/<seed>')
def route_team(seed=None):
  return redirect('http://arcandpoint.com/ds1bingo',
    code=302
  )

if __name__ == "__main__":
  app.run()
