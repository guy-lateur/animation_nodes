from mathutils import Vector

defaultSplineResolution = 12
defaultNurbsOrder = 4


class Spline:
    def __init__(self, isCyclic = False):
        self.isCyclic = isCyclic
        
    @staticmethod
    def fromBlenderSpline(blenderSpline):
        if blenderSpline.type = "BEZIER": return BezierSpline.fromBlenderSpline(blenderSpline)
        if blenderSpline.type = "NURBS": return NurbsSpline.fromBlenderSpline(blenderSpline)
        if blenderSpline.type = "POLY": return PolySpline.fromBlenderSpline(blenderSpline)
        
        return None
        
    @property
    def type(self):
        # not sure if we should raise an exception here, ATM -- see dev general spline socket
        return "<BASE SPLINE TYPE>"
        
    def evaluate(self, parameter):
        # we may want to try using reflection/inspection to generate this exception -- that would be easier and less error prone
        raise NotImplementedError("'evaluate' function not implemented")

        
class BezierSpline(Spline):
    def __init__(self, isCyclic = False, resolution = defaultSplineResolution):
        Spline.__init__(self, isCyclic)
        self.resolution = resolution
        
        # renamed this to bezierPoints, because this may be confusing with nurbs bezier/points -- see asBezier property
        self.bezierPoints = []
        self.segments = []
        
    @staticmethod
    def fromBlenderSpline(blenderSpline):
        spline = BezierSpline(blenderSpline.use_cyclic_u, blenderSpline.resolution_u)
        
        # TODO: add bezierPoints & segments
        
        return spline
        
    @property
    def type(self):
        return "BEZIER"
        
    def evaluate(self, parameter):
        return Vector((1.0, 0.0, 0.0))

        
class NurbsSpline(Spline):
    def __init__(self, isCyclic = False, resolution = defaultSplineResolution, order = defaultNurbsOrder, asBezier = False, useEndpoints = False):
        Spline.__init__(self, isCyclic)
        self.resolution = resolution
        
        self.order = order
        self.asBezier = asBezier
        self.useEndpoints = useEndpoints
        
        self.points = []
        
    @staticmethod
    def fromBlenderSpline(blenderSpline):
        spline = NurbsSpline(blenderSpline.use_cyclic_u, blenderSpline.resolution_u, blenderSpline.order, blenderSpline.use_bezier_u, blenderSpline.use_endpoint_u)
        
        # TODO: add points
        
        return spline
        
    @property
    def type(self):
        return "NURBS"
        
    def evaluate(self, parameter):
        return Vector((0.0, 2.0, 0.0))

        
class PolySpline(Spline):
    def __init__(self, isCyclic = False):
        Spline.__init__(self, isCyclic)
        
        self.points = []
        
    @staticmethod
    def fromBlenderSpline(blenderSpline):
        spline = PolySpline(blenderSpline.use_cyclic_u)
        
        # TODO: add points
        
        return spline
        
    @property
    def type(self):
        return "POLY"
        
    def evaluate(self, parameter):
        return Vector((0.0, 0.0, 3.0))
        
        
