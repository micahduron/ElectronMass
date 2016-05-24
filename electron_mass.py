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

def main():
    data = FetchData('electron_data.csv')

    print 'Mass: ', ElectronMass(data.values())
    print 'Error: ', ErrorBars(ElectronMass, data)

def ElectronMass(args):
    HgBlueAngle = abs(args['HgBlueLeft'] - args['HgBlueRight']) / 2
    HgBGAngle = abs(args['HgBGLeft'] - args['HgBGRight']) / 2

    HPurpAngle = abs(args['HyPurpLeft'] - args['HyPurpRight']) / 2
    HBGAngle = abs(args['HyBGLeft'] - args['HyBGRight']) / 2

    HPurpLambda = CalcHLambda(HPurpAngle, HgBlueAngle, HgBlueLambda)
    HBGLambda = CalcHLambda(HBGAngle, HgBGAngle, HgBGLambda)

    HPurpEnergy = PlanckC * LightSpeed / HPurpLambda
    HBGEnergy = PlanckC * LightSpeed / HBGLambda

    HPurpBohrC = CalcBohrConstant(HPurpEnergy, args['HyPurpN'])
    HBGBohrC = CalcBohrConstant(HBGEnergy, args['HyBGN'])

    AvgBohrC = (HPurpBohrC + HBGBohrC) / 2

    # This is really the reduced mass of the system.
    MeasuredMass = (2 * (ReducedPlanckC ** 2) * AvgBohrC) / ((CoulombC ** 2) * (FundCharge ** 4))

    # This is a calculation to obtain the true mass from the reduced mass.
    CorrectedMass = MeasuredMass / (1 - MeasuredMass / ProtonMass)

    return CorrectedMass

def CalcHLambda(HAngle, HgAngle, HgLambda):
    HAngleRad = math.radians(HAngle)
    HgAngleRad = math.radians(HgAngle)

    return math.sin(HAngleRad) / math.sin(HgAngleRad) * (HgLambda * 1e-9)

def CalcBohrConstant(PhotonEnergy, EnergyLevel):
    return PhotonEnergy / (1.0 / 4 - 1.0 / (EnergyLevel ** 2))

def FetchData(csvFile):
    data = Datapoints()

    with open(csvFile, 'r') as file:
        rows = csv.DictReader(file)

        for row in rows:
            data[row['Parameter']] = ProcessRow(data, row)
    return data

def ProcessRow(data, row):
    if row['Type'] == 'Angle':
        angles = map(ParseAngle, row['Data'].split(','))
        deviation = ParseAngle(row['Deviation'])

        return AverageData(angles, deviation)
    elif row['Type'] == 'Raw':
        value = float(row['Data'])
        deviation = float(row['Deviation'])

        return (value, deviation)
    raise ValueError('Invalid type value.')

def AverageData(data, deviation):
    avg = math.fsum(data) / len(data)
    dev = deviation / math.sqrt(len(data))

    return avg, dev

DegreeRegex = re.compile('^((?P<degrees>\d+)d)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?$')

def ParseAngle(degString):
    d = 0
    m = 0
    s = 0

    matches = DegreeRegex.match(degString)

    if matches is not None:
        d = GetAnglePart(matches, 'degrees')
        m = GetAnglePart(matches, 'minutes')
        s = GetAnglePart(matches, 'seconds')
    else:
        d = float(degString)

    return deg(degrees=d, minutes=m, seconds=s)

def GetAnglePart(matches, matchId, defaultVal = 0):
    matchStr = matches.group(matchId)

    return float(matchStr if matchStr is not None else defaultVal)

def deg(degrees = 0, minutes = 0, seconds = 0):
    return float(degrees + minutes / 60.0 + seconds / 3600.0)

if __name__ == '__main__':
    main()
