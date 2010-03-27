# -*- coding: utf-8 -*-

class Context(object):
    '''Context class: holds its current score, and the rules and actions related to this context'''
    def __init__(self, state):
        self.score = None
        self.rules = []
        self.in_actions = []
        self.out_actions = []
        self._state = state
    def update_score(self):
        '''Update this context score based on individual rules confidences:\nscore= 1-((1-val1)*(1-val2)*(1-val3)...)'''
        inv_score = 1
        for rule in self.rules:
            if rule.match:
                inv_score *= (1 - rule.confidence)
        self.score = 1 - inv_score
        self._state.checkmax()