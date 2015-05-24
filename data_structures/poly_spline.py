from mathutils import Vector

from . import spline
from spline import Spline


class PolySpline(Spline):
    def __init__(self, isCyclic = False):
        Spline.__init__(self, isCyclic)
        
        self.points = []
        self.segments = []
        
    @staticmethod
    def fromBlenderSpline(blenderCurve, blenderSpline):
        spline = PolySpline(blenderSpline.use_cyclic_u)
        
        for splinePoint in blenderSpline.points:
            point = Vector((splinePoint.co[0], splinePoint.co[1], splinePoint.co[2]))
            spline.points.append(point)
        
        spline.updateSegments()
        spline.transform(blenderCurve.matrix_world)
        
        return spline
        
    @property
    def nrSegments(self):
        return len(self.segments)
        
    def updateSegments(self):
        self.segments = []
        for left, right in zip(self.points[:-1], self.points[1:]):
            self.segments.append(PolySegment(left, right))
            
        if self.isCyclic:
            self.segments.append(PolySegment(self.points[-1], self.points[0]))
        
    def toSegmentsParameter(self, parameter):
        return min(max(parameter, 0), 0.9999) * len(self.segments)
        
    # base class implementation
    ###########################
             
    @property
    def type(self):
        return "POLY"
        
    @property
    def hasLength(self):
        return True
        
    def copy(self):
        spline = PolySpline(self.isCyclic)
        spline.points = [point.copy() for point in self.points]
        return spline
        
    def transform(self, matrix):
        for point in self.points:
            transformedPoint = matrix * point
            point.x = transformedPoint.x
            point.y = transformedPoint.y
            point.z = transformedPoint.z
        
    def evaluate(self, parameter):
        par = self.toSegmentsParameter(parameter)
        return self.segments[int(par)].evaluate(par - int(par))
        
    def evaluateTangent(self, parameter):
        par = self.toSegmentsParameter(parameter)
        return self.segments[int(par)].evaluateTangent(par - int(par))
        
    def project(self, point):
        parameters = [(i + segment.project(point)) / len(self.segments) for i, segment in enumerate(self.segments)]
        return curve_util.chooseNearestParameter(self, point, parameters)
    
    # could probably be implemented in base spline class -- needs project, evaluate & evaluateTangent
    def projectExtended(self, point):
        parameter = self.project(point)
        splineProjection = self.evaluate(parameter)
        splineTangent = self.evaluateTangent(parameter)
        possibleProjectionData = [(splineProjection, splineTangent)]
        
        if not self.isCyclic:
            startPoint = self.evaluate(0)
            startTangent = self.evaluateTangent(0)
            startLineProjection = curve_util.findNearestPointOnLine(startPoint, startTangent, point)
            if (startLineProjection.x - startPoint.x) / startTangent.x <= 0:
                possibleProjectionData.append((startLineProjection, startTangent))
            
            endPoint = self.evaluate(1)
            endTangent = self.evaluateTangent(1)
            endLineProjection = curve_util.findNearestPointOnLine(endPoint, endTangent, point)
            if (endLineProjection.x - endPoint.x) / endTangent.x >= 0: 
                possibleProjectionData.append((endLineProjection, endTangent))
        
        return min(possibleProjectionData, key = lambda item: (point - item[0]).length_squared)
    
    # nrSamples is ignored
    def calculateLength(self, nrSamples = 5):
        length = 0
        for segment in self.segments:
            length += segment.calculateLength()
        return length  
        
        
class PolySegment:
    def __init__(self, left, right):
        self.left = left
        self.right = right
            
    def evaluate(self, parameter):
        return self.left + (self.right - self.left) * parameter
        
    def evaluateTangent(self, parameter):
        return self.right - self.left
        
    def calculateLength(self):
        return (self.right - self.left).length
        
    def project(self, point):
        return min(1, max(0, curve_util.findNearestParameterOnLine(self.left, self.right - self.left, point)))
