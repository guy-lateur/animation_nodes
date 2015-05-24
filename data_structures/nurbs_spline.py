from . import spline
from spline import Spline


class NurbsSpline(Spline):
    def __init__(self, isCyclic = False, order = defaultNurbsOrder, asBezier = False, useEndpoints = False):
        Spline.__init__(self, isCyclic)
        
        self.order = order
        self.asBezier = asBezier
        self.useEndpoints = useEndpoints
        
        self.points = []
        
    @staticmethod
    def fromBlenderSpline(blenderCurve, blenderSpline):
        spline = NurbsSpline(blenderSpline.use_cyclic_u, blenderSpline.order, blenderSpline.use_bezier_u, blenderSpline.use_endpoint_u)
        
        # TODO: add points
        
        spline.transform(blenderCurve.matrix_world)
        return spline
        
    @property
    def type(self):
        return "NURBS"
        
    def evaluate(self, parameter):
        return Vector((0.0, 2.0, 0.0))
