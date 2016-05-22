import math

class Datapoints(object):
    def __init__(self, data = None):
        self._values = {}
        self._deviations = {}

        if data is not None:
            self.addData(data)

    def addDatapoint(self, param, value, dev):
        self._values[param] = value
        self._deviations[param] = dev

    def addData(self, data):
        for param in data.iterkeys():
            self[param] = data[param]

    def params(self):
        return self._values.iterkeys()

    def values(self):
        return DictView(self._values)

    def deviations(self):
        return DictView(self._deviations)

    def __getitem__(self, param):
        return self._values[param], self._deviations[param]

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
    originalFVal = f(data.values())

    origValue, deviation = data[parameter]

    upperValue = ModifyAndExecute(f, data, parameter, origValue + deviation)
    plusDev = abs(originalFVal - upperValue)

    lowerValue = ModifyAndExecute(f, data, parameter, origValue - deviation)
    minusDev = abs(originalFVal - lowerValue)

    return max(plusDev, minusDev)

def ModifyAndExecute(f, data, param, paramValue):
    origValue = data._values[param]
    data._values[param] = paramValue

    retVal = f(data.values())

    data._values[param] = origValue

    return retVal
