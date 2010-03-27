# -*- coding: utf-8 -*-
class State(dict):
  "Main Magellan class, holding the status of the active contexts and rules"

  def __new__(cls, *p, **k):
    if not '_singleton' in cls.__dict__:
      cls._singleton = dict.__new__(cls)
    return cls._singleton

  def __init__(self):
    self.current_context = self['Default']
    self.THRESHOLD = 0.6

  def __getitem__(self,key):
    try:
      return dict.__getitem__(self,key)
    except KeyError: #used to avoid explicitly creating a new Context object each time
      new_context = State.Context(self)
      self[key] = new_context
      return new_context

  def checkmax(self):
    "Select the more likely context based on the rules, and executes its input and output actions if needed"
    max_context = max(self.values(), key= lambda m:m.score)

    if max_context.score < self.THRESHOLD:
      max_context = self['Default']

    if max_context is not self.current_context:
      for action in self.current_context.out_actions:
        action()
      self.current_context = max_context
      for action in self.current_context.in_actions:
        action()

  def add_rule(self,source,value,context,confidence):
    "Add a rule to its context's rules and connects it to the event source"
    rule = partial(State.Rule(confidence),self[context],value)
    self[context].rules.append((source,rule))
    source(rule)