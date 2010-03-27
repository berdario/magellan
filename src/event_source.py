class EventSource():
    def __init__(self):
        self._rules = []

    def attach(self, rule):
        if not self._rules:
            start()
        if not rule in self._rules:
            self._rules.append(rule)

    def detach(self, rule):
        try:
            self._rules.remove(rule)
            if not self._rules:
                stop()
        except ValueError:
            pass
    
    def start(self):
        raise NotImplementedError
    	
    def stop(self):
        raise NotImplementedError
    

    def notify(self, data):
        for rule in self._rules:
            rule.update(data)

