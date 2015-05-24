from mathutils import Vector

defaultNurbsOrder = 4


class Spline:
    def __init__(self, isCyclic = False):
        self.isCyclic = isCyclic
        
    @staticmethod
    def fromBlenderSpline(blenderCurve, blenderSpline):
        if blenderSpline.type = "BEZIER": return BezierSpline.fromBlenderSpline(blenderCurve, blenderSpline)
        if blenderSpline.type = "NURBS": return NurbsSpline.fromBlenderSpline(blenderCurve, blenderSpline)
        if blenderSpline.type = "POLY": return PolySpline.fromBlenderSpline(blenderCurve, blenderSpline)
        
        return None
        
    # Propeties every subclass should have/override:
    ################################################
    @property
    def type(self):
        # not sure if we should raise an exception here, ATM -- see dev general spline socket
        return "<BASE SPLINE TYPE>"
        
    @property
    def hasLength(self):
        # not sure what this is meant for
        raise NotImplementedError("'hasLength' property not implemented")
        
    # Functions every subclass should have/override:
    ################################################
    def copy(self):
        raise NotImplementedError("'copy' function not implemented")
        
    def transform(self, matrix):
        raise NotImplementedError("'transform' function not implemented")
        
    def evaluate(self, parameter):
        raise NotImplementedError("'evaluate' function not implemented")
        
    def evaluateTangent(self, parameter):
        raise NotImplementedError("'evaluateTangent' function not implemented")
    
    # returns parameter
    def project(self, point):
        raise NotImplementedError("'project' function not implemented")
        
    # returns point & tangent
    def projectExtended(self, point):
        raise NotImplementedError("'projectExtended' function not implemented")
    
    # can't have samplesPerSegment here, because that would be specific to bezier
    def calculateLength(self, nrSamples):
        raise NotImplementedError("'calculateLength' function not implemented")
            
    # get multiple samples
    ######################
             
    def getSamples(self, nrSamples):
        return self.sampleFunction(self.evaluate, nrSamples)
        
    def getTangentSamples(self, nrSamples):
        return self.sampleFunction(self.evaluateTangent, nrSamples)
        
    def sampleFunction(self, function, nrSamples):
        samples = []
        for i in range(max(nrSamples - 1, 0)):
            samples.append(function(i / (nrSamples - 1)))
        samples.append(function(1))
        return samples
    
