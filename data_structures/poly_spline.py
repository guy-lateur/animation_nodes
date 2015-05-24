from . import spline
from spline import Spline


class PolySpline(Spline):
    def __init__(self, isCyclic = False):
        Spline.__init__(self, isCyclic)
        
        self.points = []
        
    @staticmethod
    def fromBlenderSpline(blenderCurve, blenderSpline):
        spline = PolySpline(blenderSpline.use_cyclic_u)
        
        # TODO: add points
        
        spline.transform(blenderCurve.matrix_world)
        return spline
        
    @property
    def type(self):
        return "POLY"
        
    def evaluate(self, parameter):
        return Vector((0.0, 0.0, 3.0))
