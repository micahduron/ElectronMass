import math

class Datapoints:
    def __init__(self):
        self.values = {}
        self.devs = {}

    def addDatapoint(self, name, value, dev):
        self.values[name] = value
        self.devs[name] = dev

    def parameters(self):
        return self.values.keys()

    def __getitem__(self, index):
        return self.values[index]

def ErrorBars(f, data):
    deviations = (CalcDeviation(f, data, p) for p in data.parameters())
    result = math.fsum(dev ** 2 for dev in deviations)

    return math.sqrt(result)

def CalcDeviation(f, data, parameter):
    originalFVal = f(data)
    originalVal = data.values[parameter]

    data.values[parameter] = originalVal + data.devs[parameter]
    plusDev = abs(originalFVal - f(data))

    data.values[parameter] = originalVal - data.devs[parameter]
    minusDev = abs(originalFVal - f(data))

    data.values[parameter] = originalVal

    return max(plusDev, minusDev)
