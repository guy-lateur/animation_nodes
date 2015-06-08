import bpy
from bpy.types import Node
import mathutils
import math
from math import *
from ... mn_node_base import AnimationNode
from ... mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling

defaultFunction = "u * v * w"

# list of safe functions for eval()
safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
             'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot',
             'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians',
             'sin', 'sinh', 'sqrt', 'tan', 'tanh']

# use the list to filter the local namespace
safe_dict = dict((k, globals().get(k, None)) for k in safe_list)

class mn_Math3DFunctionSamplerNode(Node, AnimationNode):
    bl_idname = "mn_Math3DFunctionSamplerNode"
    bl_label = "3D Function Sampler"

    def init(self, context):
        forbidCompiling()
        self.inputs.new("mn_StringSocket", "Function").string = defaultFunction
        self.inputs.new("mn_FloatListSocket", "Argument List u")
        self.inputs.new("mn_FloatListSocket", "Argument List v")
        self.inputs.new("mn_FloatListSocket", "Argument List w")
        self.outputs.new("mn_FloatListSocket", "Samples")
        allowCompiling()

    def getInputSocketNames(self):
        return {"Function" : "function",
                "Argument List u" : "argumentListU",
                "Argument List v" : "argumentListV",
                "Argument List w" : "argumentListW"}

    def getOutputSocketNames(self):
        return {"Samples" : "samples"}

    def execute(self, function, argumentListU, argumentListV, argumentListW):
        def canExecute():
            try: self.expr_args = (compile(function, __file__, 'eval'), {"__builtins__": None}, safe_dict)
            except: return False
            
            return True

        samples = []
        if not canExecute(): return samples
        
        for argumentU in argumentListU:
            safe_dict['u'] = argumentU
            
            for argumentV in argumentListV:
                safe_dict['v'] = argumentV

                for argumentW in argumentListW:
                    safe_dict['w'] = argumentW

                    try: sample = float(eval(*(self.expr_args)))
                    except: return []
                    
                    samples.append(sample)
        
        return samples
