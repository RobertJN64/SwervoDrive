class FilterReqs:
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr_name):
        return getattr(self.stream, attr_name)

    def write(self, data):
        if ('/status' not in data and
            '/prints' not in data and
            '/traceback' not in data and
            '/wheelPos' not in data and
            '/getIMUAngle' not in data):
            self.stream.write(data)
            self.stream.flush()

    def flush(self):
        self.stream.flush()

print_log = []

def lprint(*args):
    print(' '.join(map(str, args)))
    print_log.append(' '.join(map(str, args)))
