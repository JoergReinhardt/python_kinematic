import math
import numpy as np
import scipy as sp

class tdvector(np.matrix):

    def __new__(cls, input_array):
        obj = np.asarray(input_array, float).view(cls)

        return obj.T


class transformation(np.matrix):

    def __new__(cls, initial_vector, rotation_angle, rotation_axis_vector, translation_vector=None):
        instance = np.matrix(np.diagflat(np.ones(4)), float).view(cls)
        instance.initial_vector       = tdvector(initial_vector)
        instance.rotation_angle       = rotation_angle
        instance.rotation_axis_vector = tdvector(rotation_axis_vector)
        instance.translation_vector   = tdvector(translation_vector)
        instance.matrix_rotate()
        instance.matrix_translocate()

        return instance
    
    def __array_finalize__(self, instance):
        if instance is None: return
        self.initial_vector       = getattr(instance, 'initial_vector', None)
        self.rotation_angle       = getattr(instance, 'rotation_angle', None)
        self.rotation_axis_vector = getattr(instance, 'rotation_axis_vector', None)
        self.translation_vector   = getattr(instance, 'translation_vector', None)

    def matrix_rotate(self):
        c = math.cos(math.pi/180*self.rotation_angle)
        s = math.sin(math.pi/180*self.rotation_angle)

        x = self.rotation_axis_vector[0]
        y = self.rotation_axis_vector[1]
        z = self.rotation_axis_vector[2]

        self[0,0] = c+(1-c)*(x)**2
        self[0,1] = (1-c)*x*y-s*z
        self[0,2] = (1-c)*x*z+s*y

        self[1,0] = (1-c)*x*y+s*z
        self[1,1] = c+(1-c)*y**2
        self[1,2] = (1-c)*y*z-s*x

        self[2,0] = (1-c)*x*z-s*y
        self[2,1] = (1-c)*y*z+s*x
        self[2,2] = c+(1-c)*z**2

        return self

    def matrix_translocate(self):
        self[:3,3:4] = self.translation_vector

        return self

    def rotate(self):

        return self[:3,:3] * self.initial_vector
