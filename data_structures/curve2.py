from mathutils import Matrix

from . import spline
from spline import Spline

supportedSplineTypes = ["BEZIER", "NURBS", "POLY"]

class Curve:
    def __init__(self):
        self.splines = []
        
    @staticmethod
    def fromBlenderCurve(blenderCurve):
        rvCurve = Curve()
        
        for blenderSpline in blenderCurve.data.splines:
            if blenderSpline.type in supportedSplineTypes: 
                rvCurve.splines.append(Spline.fromBlenderSpline(blenderCurve, blenderSpline))
        
        return rvCurve
        
