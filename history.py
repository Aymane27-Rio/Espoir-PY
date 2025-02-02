class History:
    def __init__(self):
        self.log = []

    def append(self, message):
        self.log.append(message)

    def display(self):
        for entry in self.log:
            print(entry)
