
import numpy as np
import os
import ctypes
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the DLL file
dll_path = os.path.join(script_dir, 'brain.dll')
brain = ctypes.CDLL(dll_path)
brain.minmaxalphabeta.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
brain.minmaxalphabeta.restype = ctypes.c_float

maps = np.zeros((20, 20), dtype=np.int32)
maps[19][19]=1
maps=maps.flatten()
point = np.array([2,5])
# maps = [0] * (20*20)
# point = [2, 3]
maps=(ctypes.c_int * len(maps))(*maps)
point=(ctypes.c_int * len(point))(*point)
# print(brain.minmaxalphabeta(maps,point,1,1,-999999999,999999999))
brain.getLegalActions.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int)
]
brain.getLegalActions.restype = ctypes.c_int
actions=np.zeros((400,2), dtype=np.int32)
actions=actions.flatten()
actions =(ctypes.c_int * len(actions))(*actions)
idx=brain.getLegalActions(maps,actions )
actions=np.array(actions).reshape(400,2)[:idx,:]
print(actions)
