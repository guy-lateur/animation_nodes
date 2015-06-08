import bpy
from bpy.types import Node
import bpy
from bpy.types import Node
import math
from math import *
from ... mn_node_base import AnimationNode
from ... mn_execution import allowCompiling, forbidCompiling

defaultFunction = "u * v"

# list of safe functions for eval()
safe_list = ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
             'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot',
             'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians',
             'sin', 'sinh', 'sqrt', 'tan', 'tanh']

# use the list to filter the local namespace
safe_dict = dict((k, globals().get(k, None)) for k in safe_list)

class mn_Math2DFunctionEvaluatorNode(Node, AnimationNode):
    bl_idname = "mn_Math2DFunctionEvaluatorNode"
    bl_label = "2D Function Evaluator"

    def init(self, context):
        forbidCompiling()
        self.inputs.new("mn_StringSocket", "Function").string = defaultFunction
        self.inputs.new("mn_FloatSocket", "Argument u")
        self.inputs.new("mn_FloatSocket", "Argument v")
        self.outputs.new("mn_FloatSocket", "Result")
        allowCompiling()

    def getInputSocketNames(self):
        return {"Function" : "function",
                "Argument u" : "argumentU",
                "Argument v" : "argumentV"}

    def getOutputSocketNames(self):
        return {"Result" : "result"}

    def execute(self, function, argumentU, argumentV):
        def canExecute():
            try: self.expr_args = (compile(function, __file__, 'eval'), {"__builtins__": None}, safe_dict)
            except: return False
            
            return True

        result = 0.0
        if not canExecute(): return result

        safe_dict['u'] = argumentU
        safe_dict['v'] = argumentV
        try: result = float(eval(*(self.expr_args)))
        except: pass
        
        return result
        