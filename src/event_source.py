class EventSource():
    def __init__(self):
        self._rules = []

    def attach(self, observer):
        if not self._rules:
            start()
        if not observer in self._rules:
            self._rules.append(observer)

    def detach(self, observer):
        try:
            self._rules.remove(observer)
            if not self._rules:
                stop()
        except ValueError:
            pass
    
    def start(self):
        raise NotImplementedError
    	
    def stop(self):
        raise NotImplementedError
    

    def notify(self, data):
        for observer in self._rules:
            observer.update(data)
