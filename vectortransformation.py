import math
import numpy as np
import scipy as sp



class vector_td(np.matrix):
    """vector_td
    Basic vector Class for all threedimensional vectors, inhibited from numpy
    matrix.  'input_array' is a python list and will be convertet to an numpy
    Matrix in the transposed Form
    """

    def __new__(cls, input_array):
        """__new__
        the '__new__' operator must be taken instead of '__init__' do to
        details in the numpy implementation. '.view(cls)' returns the np.matrix
        as our new type 'vector_td'
        """
        obj = np.matrix(input_array, float).view(cls)
    
        # transposes to the matrix arithmetic order of 1 column 3 rows 
        return obj.T

    def __str__(self):
        return 'vector_td containing elements: '+str(self)



class transformation_matrix(np.matrix):
    """transformation_matrix
    gives us all purpose matrices. At it's initialisation a 4 x 4 matrix with
    ones in the upper left to lower right diagonal and zeros everywhere else.

    'rotang' takes an optionl angle in degree (scalar, float) form as it's
    rotational aplha angle around an axis.and/or a 3 x 3 matrix to it's upper
    left corner.
    
    'rotax' takes n 3 elements 'vector_td' as the normalized vector
    represedentation (projected to the axis) of the axis to rotate around.

    'travec' takes n 3 elements 'vector_td' as the translation (move linear
    along the axis) vector.

    'transformation_matrix' returns a universal 4 X 4 translocation matrix that
    can be used for rotations around arbitrary axis, translations in all
    dimensions and one-step transformations combining both.
    It can be sliced to retrieve, or set parts of it using the [vc:bc,vr:br]
    ('from column : to col, from row : to row' colums start at 1, rows at 0)
    """

    def __new__(cls, rotang=None, rotax=None, travec=None):
        """__new__
        Parameters see 'transformation_matrix'.
        All Parameters Optional, a set of nestet if's puts the transition
        vector in to its place in the top fourth if there is one and
        'obj.matrix_rotate()' is called once if there is an rotation and
        produces the upper left 3x3 part of the matrix.
        When no parameter is given it returns the empty matrix (see
        'transformation_matrix')
        """
        obj = np.matrix(np.diagflat(np.ones(4)), float).view(cls) 
        
        if travec != None or rotang or rotax != None:

            if travec != None:
                obj[:3,3:4] = travec
                
            if rotang or rotax != None:    

                if rotang:
                    obj.rotang = rotang

                if rotax != None:
                    obj.rotax  = rotax

                else:
                    obj.rotax  = vector_td([0,0,0])

                obj.matrix_rotate()
        
        else:
            print('neigther vectortd nor angle given')
       
        return obj


    def __array_finalize__(self, obj):
        """
        I didn't get this part. It's got something to do with the special way
        those arrays are implementet in numpy, connectet to the fact, that you
        have to use '__new__' and the class misses an '__init__'.
        """
        self.rotang  = getattr(obj, 'rotang', None)
        self.rotax   = getattr(obj, 'rotax' , None)
        self.travec  = getattr(obj, 'travec', None)


    def matrix_rotate(self):
        """matrix_rotate
        the 3x3 universal rotation matrix for rotations around arbitrary axis,
        wich means that rotations around all coordinate axis can be combined to
        one rotation about that arbitrary axis.
        the x,y,z components are retrieved from 'rotax', the formulas for the
        different fields get assignd directly to the parent object, since
        '__new__' put an empty 4X4 matrix allready up there.
        """
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

    def __str__(self):
        return 'Transformation Matrix mit der Matrix: '+self.name+'und vom typ type(self) '



class vector_td_position(vector_td):
    """vector_td_position
    is the class to store position vectors in. They can be rotated and
    translated with it's inbuild methods
    """

    def __new__(cls, coordinates):
        obj = vector_td(coordinates).view(cls)

        return obj


    def rotate(self, rotang, rotax):
        """rotate
        is a public class that alters the 'vector_td_position' instance of its
        parent.
        'rotang' is the rotation angle in degree form
        'rotax' is the rotation axis in normalized vector notation. It is
        expected as python list and gets altered to the appropriate type in the
        function.
        'matrix' gets an 3X3 matrix object doe to slicing.
        'result' is the vector cross product of 'matrix' and it's parent
        'vector_td_position' instance.
        Do to numpy implementation the 'result' can not just be assigned to the
        parent via slicing (or I don't know how!?), so the for loop becomes
        nescessary
        """
        matrix = transformation_matrix(rotang=rotang, rotax=vector_td(rotax))[:3,:3]
        result = matrix * self

        for i in range(len(result)):
            self[i] = result[i]

        return self    


    def transit(self, travec):
        """transit
        works pretty much like 'rotate', only with other slices of the matrix
        :)
        'result' is the sum of the matrix addition.
        """ 
        matrix = transformation_matrix(travec=vector_td(travec))[:3,3:4]
        result = matrix + np.asmatrix(self)

        for i in range(len(result)):
            self[i] = result[i]

        return self
    

    def translocate(self, rotax, rotang=0, travec=np.zeros(3)):
        """translocate
        'rotang' is the rotation angle (degree,scalar,float)
        'rotax'  is the rotational axis (normalized vector form)
        'travec'  is the vector for translation ,i.e. moving along the
        axis(normalized vector form)
        first a 4x4 matrix will be build by calling transformation_matrix (see
        there), then the transition vector gets rezized and to 4 assigned to the
        most right row.
        'result' contains the cross product wich performs rotation and
        translation around and on all axis in the same time :)
        """
        matrix    = transformation_matrix(rotang=0, rotax=vector_td(0,0,0), travec=vector_td(0,0,0))
        vector    = np.resize(self, (4,1))
        vector[3] = 1
        result    = matrix * vector

        for i in range(3):
            self[i] = result[i]

        return self


    def __str__(self):
        return 'vector_td_position: '+type(self)



class armature_element(vector_td_position):

    def __new__(cls, root, angles, length):
        obj        = vector_td_position(root).view(cls)
        obj.root   = vector_td_position(root)
        obj.angles = vector_td(angles)
        obj.length = np.resize(np.asmatrix(length), (3,1)).view(vector_td)
        obj.rotax  = obj.find_rotax()
        obj.tip    = obj.find_tip()

        return obj


    def __array_finalize__(self, obj):
        self.root    = getattr(obj, 'root'  , None)
        self.angles  = getattr(obj, 'angles', None)
        self.rotax   = getattr(obj, 'rotax' , None)
        self.length  = getattr(obj, 'length', None)
    

    def find_rotax(self):
        print (self.angles, type(self.angles))    
        result = np.asmatrix(self.angles) * (1 / np.asmatrix(self.angles))
        print (result, type(result))
        rotax  = vector_td(result)

        print (rotax, type(rotax))
        return rotax

    def find_tip(self):
         
        tip = vector_td_postition(result)

        return tip
