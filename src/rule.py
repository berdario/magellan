class Rule(object):
    '''Rule class: keeps trace of its confidence value and the current state (matched or not)\nif called checks if the state changed and, if so, prompts the context to update its score'''
    def __init__(self, confidence):
        self.match = False
        self.confidence = confidence
    def __call__(self, context, value, values):
        match = value in values
        if self.match is not match:
            self.match = match
            context.update_score()
