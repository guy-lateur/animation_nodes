from mathutils import Matrix

from . import spline
from spline import Spline

supportedSplineTypes = ["BEZIER", "NURBS", "POLY"]
identityMatrix = Matrix.Identity(4)

class Curve:
    def __init__(self, worldMatrix = identityMatrix):
        self.worldMatrix = worldMatrix
        self.splines = []
        
    @staticmethod
    def fromBlenderCurve(blenderCurve):
        rvCurve = Curve(blenderCurve.matrix_world)
        
        for blenderSpline in blenderCurve.data.splines:
            if blenderSpline.type in supportedSplineTypes: 
                rvCurve.splines.append(Spline.fromBlenderSpline(rvCurve, blenderSpline))
        
        return rvCurve
        
