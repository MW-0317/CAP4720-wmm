class Interval:
    def __init__(self, deltatime):
        self.deltatime = deltatime

class Frame(Interval):
    def __init__(self, deltatime):
        super().__init__(deltatime)

class Tick(Interval):
    def __init__(self, deltatime):
        super().__init__(deltatime)