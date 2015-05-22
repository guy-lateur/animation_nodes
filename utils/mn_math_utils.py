from .. mn_utils import *
from .. mn_cache import *
from mathutils import *
    
# matrices
###################################

def composeMatrix(location, rotation, scale):
    matrix = Matrix.Translation(location)
    matrix *= Matrix.Rotation(rotation[2], 4, 'Z')
    matrix *= Matrix.Rotation(rotation[1], 4, 'Y')
    matrix *= Matrix.Rotation(rotation[0], 4, 'X')
    matrix *= Matrix.Scale(scale[0], 4, [1, 0, 0])
    matrix *= Matrix.Scale(scale[1], 4, [0, 1, 0])
    matrix *= Matrix.Scale(scale[2], 4, [0, 0, 1])
    return matrix