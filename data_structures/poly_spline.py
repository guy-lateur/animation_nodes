from . import spline
from spline import Spline


class PolySpline(Spline):
    def __init__(self, curve, isCyclic = False):
        Spline.__init__(self, curve, isCyclic)
        
        self.points = []
        
    @staticmethod
    def fromBlenderSpline(curve, blenderSpline):
        spline = PolySpline(curve, blenderSpline.use_cyclic_u)
        
        # TODO: add points
        
        return spline
        
    @property
    def type(self):
        return "POLY"
        
    def evaluate(self, parameter):
        return Vector((0.0, 0.0, 3.0))
