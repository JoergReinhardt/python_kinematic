import math
import numpy as np
import scipy as sp



class vector(np.matrix):


    def __new__(cls, input_array):
        obj = np.matrix(input_array, float).view(cls)
    
        return obj



class transformation_matrix(np.matrix):


    def __new__(cls, rotangl=None, rotax=None, travec=None):
        obj = np.matrix(np.diagflat(np.ones(4)), float).view(cls) 
        
        if rotangl or rotax or travec:

            if rotangl:
                obj.rotangl = rotangl

            if rotax:
                obj.rotax = rotax

            if travec:
                obj.travec = travec
        
            obj.matrix_rotate()
            
        else:
            print('neigther vector nor angle given')

       
        return obj


    def __array_finalize__(self,obj):
        self.rotangl = getattr(obj, 'rotangl', None)
        self.rotax   = getattr(obj, 'rotax', None)
        self.travec  = getattr(obj, 'travec', None)


    def matrix_rotate(self):
        c = math.cos(math.pi/180*self.rotangl)
        s = math.sin(math.pi/180*self.rotangl)

        x = self.rotax[0]
        y = self.rotax[1]
        z = self.rotax[2]

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
