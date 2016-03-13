import math

def MatrixVector3Product( matrix, vector):
    
        result = [0]*3
        for i in range(3):
            result[i] = vector[0]*matrix[0][i] + vector[1]*matrix[1][i] + vector[2]*matrix[2][i]
        return result


def Scale( magnitude, matrix):
     rot = [[magnitude, 0, 0],
          [0, magnitude, 0],
          [0, 0, magnitude]]

     result = [[0 for x in range(3)] for x in range(3)]

     for i in range(3):
        for j in range(3):
            result[i][j] = matrix[i][0]*rot[0][j] + matrix[i][1]*rot[1][j] + matrix[i][2]*rot[2][j]
     return result

    # for i in range(3):
    #    for j in range(3):
    #        matrix[i][j] = result[i][j]
    

def RotateX( angle, matrix):
    rot = [[1, 0, 0],
           [0, math.cos(angle), -math.sin(angle)],
           [0, math.sin(angle), math.cos(angle)]]

    result = [[0 for x in range(3)] for x in range(3)] 

    for i in range(3):
        for j in range(3):
            result[i][j] = matrix[i][0]*rot[0][j] + matrix[i][1]*rot[1][j] + matrix[i][2]*rot[2][j]

   # for i in range(3):
   #     for j in range(3):
   #         matrix[i][j] = result[i][j]
    return result

def RotateY( angle, matrix):
    rot = [[ math.cos(angle), 0, math.sin(angle)],
           [0, 1, 0],
           [-math.sin(angle), 0, math.cos(angle)]]
    
    result = [[0 for x in range(3)] for x in range(3)] 

    for i in range(3):
        for j in range(3):
            result[i][j] = matrix[i][0]*rot[0][j] + matrix[i][1]*rot[1][j] + matrix[i][2]*rot[2][j]

    for i in range(3):
        for j in range(3):
            matrix[i][j] = result[i][j]

def RotateZ( angle, matrix):
    rot = [[math.cos(angle), -math.sin(angle),0],
           [ math.sin(angle), math.cos(angle),0],
           [0,0,1]]
    result = [[0 for x in range(3)] for x in range(3)] 

    for i in range(3):
        for j in range(3):
            result[i][j] = matrix[i][0]*rot[0][j] + matrix[i][1]*rot[1][j] + matrix[i][2]*rot[2][j]

    for i in range(3):
        for j in range(3):
            matrix[i][j] = result[i][j]