import math
import numpy

deltaParameter = 0.001
def ParameterIsZero(parameter):
    return parameter < deltaParameter

def ParameterIsOne(parameter):
    return parameter + deltaParameter > 1.0

def chooseNearestParameter(curveElement, point, parameters):
    sampledData = [(parameter, (point - curveElement.evaluate(parameter)).length_squared) for parameter in parameters]
    return min(sampledData, key = lambda item: item[1])[0]   

def findNearestPointOnLine(linePosition, lineDirection, point):
    lineDirection = lineDirection.normalized()
    dotProduct = lineDirection.dot(point - linePosition)
    return linePosition + (lineDirection * dotProduct)
    
defaultDeltaImaginary = 0.00001
def complexToRealFloat(complex, deltaImaginary = defaultDeltaImaginary):
    try:
        if type(complex) is numpy.float_: return float(complex)
        
        if type(complex) is numpy.complex_:
            if math.fabs(complex.imag) < deltaImaginary: return float(complex.real)
    except: return None

def rootsToParameters(roots):
    realRoots = []
    for root in roots:
        realRoot = complexToRealFloat(root, deltaImaginary = deltaParameterImaginary)
        if realRoot is None: continue
        
        realRoots.append(realRoot)
    
    rvParameters = []
    doZero = False
    doOne = False
    for realRoot in realRoots:
        if ParameterIsZero(realRoot):
            doZero = True
            continue
        if ParameterIsOne(realRoot):
            doOne = True
            continue
            
        rvParameters.append(realRoot)
        
    if doZero: rvParameters.append(0.0)
    if doOne: rvParameters.append(1.0)
    
    return rvParameters
