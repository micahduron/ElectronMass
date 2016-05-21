import math

class Datapoints:
    def __init__(self, data = None):
        self.values_ = {}
        self.deviations_ = {}

        if data is not None:
            self.addData(data)

    def addDatapoint(self, param, value, dev):
        self.values_[param] = value
        self.deviations_[param] = dev

    def addData(self, data):
        for param in data.keys():
            value, deviation = data[param]

            self.addDatapoint(param, value, deviation)

    def parameters(self):
        return self.values_.iterkeys()

    def __getitem__(self, param):
        return self.values_[param]

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
