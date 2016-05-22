#!/usr/bin/env python

import math

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

def AverageData(data, deviation):
    avg = float(sum(data)) / len(data)
    dev = deviation / math.sqrt(len(data))

    return avg, dev

def deg(degrees = 0, minutes = 0, seconds = 0):
    return float(degrees + minutes / 60.0 + seconds / 3600.0)

def main():
    data = Datapoints()

    AngleDev = deg(minutes=2)

    data['HgBlueLeft']  = AverageData((deg(164,49), deg(164,48), deg(164,46)), AngleDev)
    data['HgBlueRight'] = AverageData((deg(195,22), deg(195,19), deg(195,20)), AngleDev)

    data['HgBGLeft']    = AverageData((deg(162,47), deg(162,47), deg(162,45)), AngleDev)
    data['HgBGRight']   = AverageData((deg(197,19), deg(197,18)), AngleDev)

    data['HPurpLeft']   = AverageData((deg(164,50), deg(164,50), deg(164,50)), AngleDev)
    data['HPurpRight']  = AverageData((deg(195,13), deg(195,14)), AngleDev)

    data['HPurpN']      = (5, 0)

    data['HBGLeft']     = AverageData((deg(197,5), deg(197,6), deg(197,6)), AngleDev)
    data['HBGRight']    = AverageData((deg(162,59), deg(162,59), deg(162,59)), AngleDev)

    data['HBGN']        = (4, 0)

    print 'Mass: ', ElectronMass(data.values())
    print 'Error: ', ErrorBars(ElectronMass, data)

if __name__ == '__main__':
    main()
