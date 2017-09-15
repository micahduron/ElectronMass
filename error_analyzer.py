import sys
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

class DictView(object):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

def ErrorBars(f, data):
    deviations = (CalcDeviation(f, data, p) for p in data.params())
    result = math.fsum(dev ** 2 for dev in deviations)

    return math.sqrt(result)

def CalcDeviation(f, data, parameter):
    derivative = CalcDerivative(f, data, parameter)

    return derivative * data._deviations[parameter]

# Used in CalcDerivative to calculate the optimal value of h.
InitH = math.pow(sys.float_info.epsilon, 1.0 / 3)

def CalcDerivative(f, data, parameter):
    paramValue = data._values[parameter]

    # Numerical differentiation via two-sided difference quotient
    # Special thanks to Karen Kopecky
    # Paper: http://www.karenkopecky.net/Teaching/eco613614/Notes_NumericalDifferentiation.pdf
    hPrime = InitH * max(abs(paramValue), 1)
    h = ((paramValue + hPrime) - (paramValue - hPrime)) / 2

    rightValue = ModifyAndExecute(f, data, parameter, paramValue + h)
    leftValue = ModifyAndExecute(f, data, parameter, paramValue - h)

    return (rightValue - leftValue) / (2 * h)

def ModifyAndExecute(f, data, param, paramValue):
    origValue = data._values[param]
    data._values[param] = paramValue

    retVal = f(data.values())

    data._values[param] = origValue

    return retVal
