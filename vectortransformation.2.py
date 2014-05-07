import math
import numpy as np
import scipy as sp



class vector(np.matrix):


    def __new__(cls, input_array):
        obj = np.matrix(input_array, float).view(cls)
    
        return obj.T



class transformation_matrix(np.matrix):


    def __new__(cls, rotang=None, rotax=None, travec=None):
        obj = np.matrix(np.diagflat(np.ones(4)), float).view(cls) 
        
        if travec != None or rotang or rotax != None:

            if travec != None:
                obj[:3,3:4] = travec
                
            if rotang or rotax != None:    

                if rotang:
                    obj.rotang = rotang

                if rotax != None:
                    obj.rotax = rotax

                else:
                    obj.rotax = vector([0,0,0])

                obj.matrix_rotate()
        
        else:
            print('neigther vector nor angle given')
       
        return obj


    def __array_finalize__(self,obj):
        self.rotang = getattr(obj, 'rotang', None)
        self.rotax   = getattr(obj, 'rotax', None)
        self.travec  = getattr(obj, 'travec', None)


    def matrix_rotate(self):
        c = math.cos(math.pi/180*self.rotang)
        s = math.sin(math.pi/180*self.rotang)

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



class point(vector):


    def __new__(cls, x, y, z):
        obj = vector([x,y,z]).view(cls)

        return obj


    def rotate(rotang, rotax):
        self = transformation_matrix(rotang=rotang,rotax=rotax)[:3,:3] * self 
