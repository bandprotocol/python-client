import time

class RealClock(object):
    def get_time(self):
        return int(time.time())


class MockClock(object):
    def __init__(self, current_time):
        self.current_time = current_time

    def set_time(self, current_time):
        self.current_time = current_time

    def get_time(self):
        return self.current_time


class Config(object):
    def __init__(self, endpoint, clock):
        self.endpoint = endpoint
        self.clock = clock
