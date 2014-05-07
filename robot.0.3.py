import math
dimensions = range(3)

def projection_factor (angle):
    alength = math.cos(math.radians(angle))
    blength = math.sin(math.radians(angle))
    factor = [alength,blength]
    return factor

def generate_projection (coordinate,dimension,angle):

    plengths = projection_factor(angle)

    if dimension == 0:
        xfactor = 1.0
        yfactor = plengths[0] * coordinate[1]
        zfactor = plengths[1] * coordinate[2]
    elif dimension == 1:
        xfactor = plengths[1] * coordinate[0]
        yfactor = 1.0
        zfactor = plengths[0] * coordinate[2]
    elif dimension == 2:    
        xfactor = plengths[0] * coordinate[0]
        yfactor = plengths[1] * coordinate[1]
        zfactor = 1.0
    
    shiftcoordinate = [xfactor,yfactor,zfactor]
    return shiftcoordinate

def generate_matrice (coordinates,angles):
    matrice = []
    for dim in dimensions:
        coordinate = coordinates[dim]
        dimension = dimensions[dim]
        angle = angles[dim]
        matrice.append(genereate_projection(coordinate,dimension,angle))
    return matrice

def vectorproduct (matrice):
    vectorprodukt = []
    for dim in dimensions:
        vectorproduct.append(

        )
