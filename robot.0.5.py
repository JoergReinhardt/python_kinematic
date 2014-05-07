import math
import numpy as np
import scipy as sp

alpha_angle = 45.
axis_vector = np.asarray([1,0,0],float)
point_vector = np.asarray([0,1,0],float)

class tdvector(np.matrix):

    def __new__(cls, input_array):
        obj = np.asarray(input_array, float).view(cls)
        return obj.T


class rotate_matrix(np.matrix):

    def __new__(cls, axis_vector, alpha_angle):
        obj = np.matrix(np.zeros((3,3), float)).view(cls)
        obj.axis_vector = axis_vector
        obj.alpha_angle = alpha_angle
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.axis_vector = getattr(obj, 'axis_vector', None)
        self.alpha_angle = getattr(obj, 'alpha_angle', None)

    def rotate(self):
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


class rotate_vector(rotate_matrix):

    def __new__(cls, axis_vector, alpha_angle, point_vector):
        obj = rotate_matrix(axis_vector, alpha_angle)
        obj.axis_vector = axis_vector
        obj.alpha_angle = alpha_angle
        obj.point_vector = point_vector
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.axis_vector = getattr(obj, 'axis_vector', None)
        self.alpha_angle = getattr(obj, 'alpha_angle', None)
        self.point_vector = getattr(obj, 'point_vector', None)

    def rotate_vector(self):
        unimatrix = self.rotate()
        print(unimatrix)


