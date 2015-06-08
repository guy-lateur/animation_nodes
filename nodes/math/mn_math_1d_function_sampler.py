import bpy
from bpy.types import Node
import math
from math import *
from ... mn_node_base import AnimationNode
from ... mn_execution import allowCompiling, forbidCompiling

defaultFunction = "u"

# list of safe functions for eval()
safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
             'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot',
             'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians',
             'sin', 'sinh', 'sqrt', 'tan', 'tanh']

# use the list to filter the local namespace
safe_dict = dict((k, globals().get(k, None)) for k in safe_list)

class mn_Math1DFunctionSamplerNode(Node, AnimationNode):
    bl_idname = "mn_Math1DFunctionSamplerNode"
    bl_label = "1D Function Sampler"

    def init(self, context):
        forbidCompiling()
        self.inputs.new("mn_StringSocket", "Function").string = defaultFunction
        self.inputs.new("mn_FloatListSocket", "Argument List u")
        self.outputs.new("mn_FloatListSocket", "Samples")
        allowCompiling()

    def getInputSocketNames(self):
        return {"Function" : "function",
                "Argument List u" : "argumentListU"}

    def getOutputSocketNames(self):
        return {"Samples" : "samples"}

    def execute(self, function, argumentListU):
        def canExecute():
            try: self.expr_args = (compile(function, __file__, 'eval'), {"__builtins__": None}, safe_dict)
            except: return False
            
            return True

        samples = []
        if not canExecute(): return samples
        
        for argumentU in argumentListU:
            safe_dict['u'] = argumentU
            
            try: sample = float(eval(*(self.expr_args)))
            except: return []
            
            samples.append(sample)
        
        return samples
