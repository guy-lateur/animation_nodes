import numpy
from mathutils import Vector, Matrix
from numpy.polynomial import Polynomial

from . import spline
from spline import Spline

identityMatrix = Matrix.Identity(4)
delta = 0.00001


class BezierSpline(Spline):
    def __init__(self, curve, isCyclic = False):
        Spline.__init__(self, curve, isCyclic)
        
        # renamed this to bezierPoints, because this may be confusing with nurbs bezier/points -- see asBezier property
        self.bezierPoints = []
        self.segments = []
        
    @staticmethod
    def fromBlenderSpline(curve, blenderSpline):
        spline = BezierSpline(curve, blenderSpline.use_cyclic_u)
        
        # TODO: add bezierPoints & segments
        
        return spline
        
    @property
    def type(self):
        return "BEZIER"
        
    def evaluate(self, parameter):
        return Vector((1.0, 0.0, 0.0))
