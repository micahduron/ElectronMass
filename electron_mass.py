#!/usr/bin/env python

import math
import csv
import re

from error_analyzer import *

PlanckC = 6.6261e-34
ReducedPlanckC = PlanckC / (2 * math.pi)
CoulombC = 8.9876e9
LightSpeed = 2.9979e8
FundCharge = 1.6022e-19
ProtonMass = 1.6726e-27

HgBlueLambda = 435.833
HgBGLambda = 491.604

def ElectronMass(args):
    HgBlueAngle = abs(args['HgBlueLeft'] - args['HgBlueRight']) / 2
    HgBGAngle = abs(args['HgBGLeft'] - args['HgBGRight']) / 2

    HPurpAngle = abs(args['HPurpLeft'] - args['HPurpRight']) / 2
    HBGAngle = abs(args['HBGLeft'] - args['HBGRight']) / 2

    HPurpLambda = CalcHLambda(HPurpAngle, HgBlueAngle, HgBlueLambda)
    HBGLambda = CalcHLambda(HBGAngle, HgBGAngle, HgBGLambda)

    HPurpEnergy = PlanckC * LightSpeed / HPurpLambda
    HBGEnergy = PlanckC * LightSpeed / HBGLambda

    HPurpBohrC = CalcBohrConstant(HPurpEnergy, args['HPurpN'])
    HBGBohrC = CalcBohrConstant(HBGEnergy, args['HBGN'])

    AvgBohrC = (HPurpBohrC + HBGBohrC) / 2

    MeasuredMass = (2 * (ReducedPlanckC ** 2) * AvgBohrC) / ((CoulombC ** 2) * (FundCharge ** 4))

    CalculatedMass = MeasuredMass / (1 - MeasuredMass / ProtonMass)

    return CalculatedMass

def CalcHLambda(HAngle, HgAngle, HgLambda):
    HAngleRad = math.radians(HAngle)
    HgAngleRad = math.radians(HgAngle)

    return math.sin(HAngleRad) / math.sin(HgAngleRad) * (HgLambda * 1e-9)

def CalcBohrConstant(PhotonEnergy, EnergyLevel):
    return PhotonEnergy / (1.0 / 4 - 1.0 / (EnergyLevel ** 2))

def FetchData(csvFile):
    data = Datapoints()

    with open(csvFile, 'r') as file:
        rows = csv.DictReader(file, restkey='dataVals')

        for row in rows:
            dataVals = map(ParseDegree, row['dataVals'])
            deviation = ParseDegree(row['Deviation'])

            data[row['Parameter']] = AverageData(dataVals, deviation)
    return data

def AverageData(data, deviation):
    avg = math.fsum(data) / len(data)
    dev = deviation / math.sqrt(len(data))

    return avg, dev

DegreeRegex = re.compile('^(?P<degrees>\d+)?(\'(?P<minutes>\d+))?(\'\'(?P<seconds>\d+))?$')

def ParseDegree(degString):
    matches = DegreeRegex.match(degString)

    # Assume searchResults returns something valid for now

    d = GetAnglePart(matches, 'degrees')
    m = GetAnglePart(matches, 'minutes')
    s = GetAnglePart(matches, 'seconds')

    return deg(degrees=d, minutes=m, seconds=s)

def GetAnglePart(matches, matchId, defaultVal = 0):
    matchStr = matches.group(matchId)

    return float(matchStr if matchStr is not None else defaultVal)

def deg(degrees = 0, minutes = 0, seconds = 0):
    return float(degrees + minutes / 60.0 + seconds / 3600.0)

def main():
    data = FetchData('electron_data.csv')

    print 'Mass: ', ElectronMass(data.values())
    print 'Error: ', ErrorBars(ElectronMass, data)

if __name__ == '__main__':
    main()
