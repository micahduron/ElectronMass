import math

class Datapoints:
    def __init__(self, data = None):
        self.values_ = {}
        self.deviations_ = {}

        if data is not None:
            self.addData(data)

    def addDatapoint(self, name, value, dev):
        self.values_[name] = value
        self.deviations_[name] = dev

    def addData(self, data):
        for k in data.keys():
            point = data[k]

            self.addDatapoint(k, point[0], point[1])

    def parameters(self):
        return self.values_.iterkeys()

    def __getitem__(self, index):
        return self.values_[index]

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
