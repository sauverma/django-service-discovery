class ServiceDiscoError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ServiceRegDeregError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ConsulClientError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)