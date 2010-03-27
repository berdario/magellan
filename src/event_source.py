class EventSource():
    def __init__(self):
        self._rules = []

    def attach(self, rule):
        if not rule in self._rules:
            self._rules.append(rule)

    def detach(self, rule):
        try:
            self._rules.remove(rule)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for rule in self._rules:
            if modifier != rule:
                rule.update(self.data())

    def data(self):
        raise NotImplementedError
