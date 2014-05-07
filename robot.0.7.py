import math
import numpy as np
import scipy as sp

alpha = 45.0
axvec = np.asarray([0,1,0],float)
posvec = np.asarray([1,0,0],float)

class tdvector(np.matrix):

    def __new__(cls, input_array):
        obj = np.asarray(input_array, float).view(cls)
        return obj.T


class rotate_matrix(np.matrix):

    def __new__(cls, alpha_angle, axis_vector, position_vector):
        obj                 = np.matrix(np.zeros((3,3), float)).view(cls)
        obj.alpha_angle     = alpha_angle
        obj.axis_vector     = tdvector(axis_vector)
        obj.position_vector = tdvector(position_vector)
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.alpha_angle = getattr(obj, 'alpha_angle', None)
        self.axis_vector = getattr(obj, 'axis_vector', None)
        self.position_vector = getattr(obj, 'position_vector', None)

    def matrix_rotate(self):
        c = math.cos(math.pi/180*self.alpha_angle)
        s = math.sin(math.pi/180*self.alpha_angle)

        ax = self.axis_vector[0]
        ay = self.axis_vector[1]
        az = self.axis_vector[2]

        self[0,0] = c+(1-c)*(ax)**2
        self[0,1] = (1-c)*ax*ay-s*az
        self[0,2] = (1-c)*ax*az+s*ay

        self[1,0] = (1-c)*ax*ay+s*az
        self[1,1] = c+(1-c)*ay**2
        self[1,2] = (1-c)*ay*az-s*ax

        self[2,0] = (1-c)*ax*az-s*ay
        self[2,1] = (1-c)*ay*az+s*ax
        self[2,2] = c+(1-c)*az**2

        return self


    def position_rotate(self):
        unimatrix = self.matrix_rotate()
        return unimatrix * self.position_vector

