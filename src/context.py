# -*- coding: utf-8 -*-
from netsource import Network
from functools import partial
from time import sleep
import loader

class Context(object):
  "Context class: holds its current score, and the rules and actions related to this context"
  def __init__(self, state):
    self.__dict__['score'] = None
    self.rules = []
    self.in_actions = []
    self.out_actions = []
    self._state = state
  def __setattr__(self,name,value):
    self.__dict__[name]=value
    if name == 'score':
      self._state.checkmax() #every time the score is updated the most likely context is recalculated, but now the score is updated only in one place, so it's not very useful
  def update_score(self):
    "Update this context score based on individual rules confidences:\nscore= 1-((1-val1)*(1-val2)*(1-val3)...)"
    self.score = 1-reduce(float.__mul__,(1-rule.func.confidence for source,rule in self.rules if rule.func.match),1.0)

def in_casa():
  print "sono a casa"

def out_casa():
  print "esco di casa"

def default():
  print "contesto di default"