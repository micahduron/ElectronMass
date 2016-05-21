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
        for param in data.iterkeys():
            self[param] = data[param]

    def params(self):
        return self.values_.iterkeys()

    def values(self):
        return DictView(self.values_)

    def deviations(self):
        return DictView(self.deviations_)

    def __getitem__(self, param):
        return self.values_[param], self.deviations_[param]

    def __setitem__(self, param, datapoint):
        value, deviation = datapoint

        self.addDatapoint(param, value, deviation)

    def __iter__(self):
        for param in self.params():
            value, deviation = self[param]

            yield param, value, deviation

class DictView:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

def ErrorBars(f, data):
    deviations = (CalcDeviation(f, data, p) for p in data.params())
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
