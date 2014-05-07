import Transformations as tr
import numpy as np



class vector(np.ndarray):

    def __new__(cls, coordinates=[]):

        obj           = np.array(np.zeros(4), float).reshape(4,1).view(cls)
        leng          = coordinates.__len__()
        obj[:leng,:1] = np.asarray(coordinates, float).reshape(leng,1).view(cls)

        return obj


    def __array_finalize__(self, obj):

        if obj is None: return
    

    def toggle_rot(self):

        self[:4,:1] = 0.0

        return self


    def toggle_trans(self):

        self[:4,:1] = 1.0

        return self

class structure(object):
    def rotate(eulerangle):
        pass

class segment(structure):
    def __init__(self, parent = None, length=1, orient=np.eye(4).view(np.matrix), name = ""):
        self.parent = parent
        self.lenght = length
        self.orient = orient
        self.name = name
        
        self.child = None
        self.parent.setChild(self)
        
    def setChild(self, child):
        self.child = child
    
    def rotate(eulerangle):
        #dieses Element rotieren
        #es wird hier einfach die orientierung geändert
        pass

    def addChild(self, segment):
        if self.child == None:
            self.child == segment
            return segment
        else:
            print "Es ist hier nur möglich eine Schlange zu bauen"
            
    def getChild(self):
        return self.child
        
    def __str__(self):
        print self.name

    def getLocalCoordinates(self):
        if self. parent == None:
            endpoint = vector()
        else:
            startpoint, endpoint = self.child.getLocalCoordinates()
        #translationVector = self.length.einheitsvektor.roation
        startpoint = endpoint
        endpoint = endpoint + translationVector
        return startpoint, endpoint
        
        
        return startpoint, endpoint

class armature(structure):

    def __init__(self, chain=0, orient=np.eye(4).view(np.matrix), length=0, origin=vector()):

        self.chains   = []
        self.orients  = []
        self.lengths  = []
        self.origin    = []
        self.chains.append(chain)
        self.orients.append(orient)
        self.lengths.append(length)
        self.origin.append(origin)
        
        self.rootElement = None

        return None

    def getLastSegment(self):
        child = self.rootElement
        while child != None:
            if child.getChild() == None:
                return child
            else:
                child = child.getChild()
        return child #Diese Zeile nur bis nichts besseres eingefallen ist

    def addSegment(self, segment):
        if self.rootElement == None:
            self.rootElement = segment
            return segment
            
        lastSegment = self.getLastSegment()
        return lastSegment.addChild(segment)
        
        

    def getWorldCoordinates(self):
        pass

    def append(self, orient=np.eye(4).view(np.matrix), length=0, root=vector((0,0,0))):

        chainlen = self.chains.__len__()

        self.chains.append(chainlen)
        self.orients.append(orient)
        self.lengths.append(length)
        self.roots.append(root)

        return self


    def translate(self, chainpos, angle, axis):
        """Eigentlich eine transrotate funktion
        Zuerst wird translatiert dann rotiert
        
        """

        if chainpos == 1:

            RotMat  = tr.rotation_matrix(angle, axis)

            oldori  = self.orients[0]
            newori  = np.dot(RotMat,oldori)

            self.orients[0] = newori

            return self


        if chainpos > 1:

            point   = self.roots[chainpos-1] # hier ändern
            RotMat  = tr.rotation_matrix(angle, axis, point)

            oldroot = self.roots[chainpos-1].toggle_trans()
            newroot = np.dot(RotMat,oldroot)[:3,:1] # mal länge

            oldori  = self.orients[chainpos-1]()
            newori  = np.dot(tr.unit_vector(RotMat),oldori)

            self.roots[chainpos-1]   = newroot
            self.orients[chainpos] = newori

            return self
