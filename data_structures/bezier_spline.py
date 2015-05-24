import numpy
from mathutils import Vector, Matrix
from numpy.polynomial import Polynomial

from . import spline
from . import curve_util
from spline import Spline

identityMatrix = Matrix.Identity(4)
delta = 0.00001


class BezierSpline(Spline):
    def __init__(self, isCyclic = False):
        Spline.__init__(self, isCyclic)
        
        # renamed this to bezierPoints, because this may be confusing with nurbs bezier/points -- see asBezier property
        self.bezierPoints = []
        self.segments = []
        
    @staticmethod
    def fromBlenderSpline(blenderCurve, blenderSpline):
        spline = BezierSpline(blenderSpline.use_cyclic_u)
        
        for blenderPoint in blenderSpline.bezier_points:
            point = BezierPoint.fromBlenderPoint(blenderPoint)
            spline.bezierPoints.append(point)
        
        spline.updateSegments()
        spline.transform(blenderCurve.matrix_world)
        
        return spline
        
    @property
    def nrSegments(self):
        return len(self.segments)
        
    def updateSegments(self):
        self.segments = []
        for left, right in zip(self.bezierPoints[:-1], self.bezierPoints[1:]):
            self.segments.append(BezierSegment(left, right))
            
        if self.isCyclic:
            self.segments.append(BezierSegment(self.bezierPoints[-1], self.bezierPoints[0]))
        
    def toSegmentsParameter(self, parameter):
        return min(max(parameter, 0), 0.9999) * len(self.segments)
        
    def toSamplesPerSegment(self, nrSamples):
        if self.nrSegments < 2: return nrSamples
        
        samplesPerSegment = nrSamples / self.nrSegments
        if samplesPerSegment < 2: samplesPerSegment = 2
        
        return samplesPerSegment
        
    def calculateSmoothHandles(self, strength = 1):
        neighborSegments = self.getNeighborSegments()
        for segment in neighborSegments:
            segment.calculateSmoothHandles(strength)
            
    def getNeighborSegments(self):
        bezierPoints = self.bezierPoints
        if len(bezierPoints) < 2: return []
        neighborSegments = []
        if self.isCyclic:
            for i, point in enumerate(bezierPoints):
                segment = BezierNeighbors(bezierPoints[i-2].location, bezierPoints[i-1], point.location)
                neighborSegments.append(segment)
        else:
            neighborSegments.append(BezierNeighbors(bezierPoints[0].location, bezierPoints[0], bezierPoints[1].location))
            neighborSegments.append(BezierNeighbors(bezierPoints[-2].location, bezierPoints[-1], bezierPoints[-1].location))
            for before, point, after in zip(bezierPoints[:-2], bezierPoints[1:-1], bezierPoints[2:]):
                neighborSegments.append(BezierNeighbors(before.location, point, after.location))
        return neighborSegments
        
    # base class implementation
    ###########################
             
    @property
    def type(self):
        return "BEZIER"
        
    @property
    def hasLength(self):
        return True
        
    def copy(self):
        spline = BezierSpline(self.isCyclic)
        spline.bezierPoints = [bezierPoint.copy() for bezierPoint in self.bezierPoints]
        return spline
        
    def transform(self, matrix):
        for bezierPoint in self.bezierPoints:
            bezierPoint.transform(matrix)
        
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
        
    def calculateLength(self, nrSamples = 5):
        samplesPerSegment = self.toSamplesPerSegment(nrSamples)
        length = 0
        for segment in self.segments:
            length += segment.calculateLength(samplesPerSegment)
        return length  
        
        
class BezierSegment:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
        self.coeffs = [
            left.location,
            left.location * (-3.0) + left.rightHandle * (+3.0),
            left.location * (+3.0) + left.rightHandle * (-6.0) + right.leftHandle * (+3.0),
            left.location * (-1.0) + left.rightHandle * (+3.0) + right.leftHandle * (-3.0) + right.location]
            
    def evaluate(self, parameter):
        c = self.coeffs
        return c[0] + parameter * (c[1] + parameter * (c[2] + parameter * c[3]))
        
    def evaluateTangent(self, parameter):
        c = self.coeffs
        return c[1] + parameter * (c[2] * 2 + parameter * c[3] * 3)
        
    def calculateLength(self, nrSamples = 5):
        length = 0
        last = self.evaluate(0)
        for i in range(nrSamples - 1):
            parameter = (i + 1) / (nrSamples - 1)
            current = self.evaluate(parameter)
            length += (current - last).length
            last = current
        return length
        
    def project(self, point):
        return curve_util.chooseNearestParameter(self, point, self.findRootParameters(point))
    
    # http://jazzros.blogspot.be/2011/03/projecting-point-on-bezier-curve.html    
    def findRootParameters(self, coordinates):
        left = self.left
        right = self.right
        
        p0 = left.location - coordinates
        p1 = left.rightHandle - coordinates
        p2 = right.leftHandle - coordinates
        p3 = right.location - coordinates
        
        a = p3 - 3 * p2 + 3 * p1 - p0
        b = 3 * p2 - 6 * p1 + 3 * p0
        c = 3 * (p1 - p0)
        
        coeffs = [0] * 6
        coeffs[0] = c.dot(p0)
        coeffs[1] = c.dot(c) + b.dot(p0) * 2.0
        coeffs[2] = b.dot(c) * 3.0 + a.dot(p0) * 3.0
        coeffs[3] = a.dot(c) * 4.0 + b.dot(b) * 2.0
        coeffs[4] = a.dot(b) * 5.0
        coeffs[5] = a.dot(a) * 3.0
        
        poly = Polynomial(coeffs, [0.0, 1.0], [0.0, 1.0])
        roots = poly.roots()
        realRoots = curve_util.rootsToParameters(roots)

        return realRoots
        
        
class BezierNeighbors:                
    def __init__(self, leftLocation, point, rightLocation):
        self.point = point
        self.leftLocation = leftLocation
        self.rightLocation = rightLocation
        
    # http://www.antigrain.com/research/bezier_interpolation/          
    def calculateSmoothHandles(self, strength = 1):
        co = self.point.location
        distanceBefore = (co - self.leftLocation).length
        distanceAfter = (co - self.rightLocation).length
        proportion = distanceBefore / max(distanceBefore + distanceAfter, 0.00001)
        handleDirection = (self.rightLocation - self.leftLocation).normalized()
        self.point.leftHandle = co - handleDirection * proportion * strength
        self.point.rightHandle = co + handleDirection * proportion * strength
        
        
class BezierPoint:
    def __init__(self):
        self.location = Vector((0, 0, 0))
        self.leftHandle = Vector((0, 0, 0))
        self.rightHandle = Vector((0, 0, 0))
        
    @staticmethod
    def fromBlenderPoint(blenderPoint):
        point = BezierPoint()
        point.location = blenderPoint.co
        point.leftHandle = blenderPoint.handle_left
        point.rightHandle = blenderPoint.handle_right
        return point
        
    @staticmethod
    def fromLocation(location):
        point = BezierPoint()
        point.location = location
        return point
        
    def copy(self):
        point = BezierPoint()
        point.location = self.location.copy()
        point.leftHandle = self.leftHandle.copy()
        point.rightHandle = self.rightHandle.copy()
        return point    

    def transform(self, matrix = identityMatrix):
        self.location = matrix * self.location
        self.leftHandle = matrix * self.leftHandle
        self.rightHandle = matrix * self.rightHandle
