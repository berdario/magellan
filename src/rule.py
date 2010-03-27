class Rule(object):
    '''Rule class: keeps trace of its confidence value and the current state (matched or not)\nif called checks if the state changed and, if so, prompts the context to update its score'''
    def __init__(self, field, operation, operator, event_source_name,
                  confidence):
        self.latest_match = False
        self.context = None # it's set later
        self.field = field
        self.confidence = confidence
        self.operation = operation
        self.operator = operator
        try:
            self.event_source = globals()[event_source_name]
        except Exception, exc:
            raise RuntimeError("There is no event source named " +
                                event_source_name)

    def notify(self):
        current_match = self.matches()
        if current_match != self.latest_match:
            #do something
            self.context.update_score(self)
        self.latest_match = current_match

    def matches(self):
        data = self.event_source.data()
        if data.key(self.field):
            value = data[self.field]
            if value == self.operator:
                return True
            else:
                return False
        else:
            # this event source doesn't provide this field -> return False
            return False