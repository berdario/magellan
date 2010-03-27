class EventSource():
    def __init__(self):
        self._rules = []

    def attach(self, observer):
        if not observer in self._rules:
            self._rules.append(observer)

    def detach(self, observer):
        try:
            self._rules.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._rules:
            if modifier != observer:
                observer.update(self)
                
    def data(self):
        raise NotImplementedError