import math
length = 1
angles = [0.0,0.0,0.0]
dimensions = range(3)
coordinate = [1.0,1.0,1.0]
coordinates = []

def projectionlength (angle):
    alength = math.cos(math.radians(angle))
    blength = math.sin(math.radians(angle))
    factor = [alength,blength]
    return factor

def flatrotate (coordinate,dimension,angle):

    plengths = projectionlength(angle)

    if dimension == 0:
        xfactor = 1
        yfactor = plengths[0] * coordinate[1]
        zfactor = plengths[1] * coordinate[2]
    elif dimension == 1:
        xfactor = plengths[1] * coordinate[0]
        yfactor = 1
        zfactor = plengths[0] * coordinate[2]
    elif dimension == 2:    
        xfactor = plengths[0] * coordinate[0]
        yfactor = plengths[1] * coordinate[1]
        zfactor = 1
    
    coordinate = [xfactor,yfactor,zfactor]
    return coordinate

def deeprotate (coordinates,angles):
    i = 0
    for angle in angles:
        coordinate = coordinates[i]
        dimension = dimensions[i]
        angle = angles[i]
        flatrotate(coordinate,dimension,angle)
