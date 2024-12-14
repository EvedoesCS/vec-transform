# ========================================= #
# Program: Given a 3d object project it
# isometrically into 2d and view it under a
# constant rotation in 2d space;
# ========================================= #
# Algorithm:
'''
Given a matrix of verticies for a 3d shape:
    1. Apply a rotation transformation to each verticie
    2. Project the vertex into R^2 space isometrically
    3. Convert the coordinates into pixel space [drawn from the
       top left corner (0, 0)]
    4. Connect each vertex with a series of lines to render it
    5. Repeat over an interval to view a "Constant transformation"
       like effect.
'''

import graphics as graphPy
import math
from random import choice
from time import sleep


def rotateIn3D(angle, shape):
    '''
    Pre: angle is the angle to rotate the shape by. Shape is a
    matrix coresponding to verticies of a 3D object;
    Purpose: Rotate a matrix of verticies about the x, y, and z axes;
    Post: Return a matrix of the rotated verticies;
    '''
    rotX = rotateAboutXaxis(angle[0], shape)
    rotY = rotateAboutXaxis(angle[1], rotX)
    rotZ = rotateAboutXaxis(angle[2], rotY)

    return rotZ


def rotateAboutXaxis(angle, shape):
    '''
    Pre: angle is the angle to rotate by,
    shape is a matrix of verticies to rotate;
    Purpose: Rotate the veticies about the X-axis;
    Post: Return the rotated matrix of verticies;
    '''
    theta = math.radians(angle)
    rotationMatrix = [[1, 0, 0],
                      [0, math.cos(theta), (-1 * math.sin(theta))],
                      [0, math.sin(theta), math.cos(theta)]]

    # Perform matrix multiplication for each vertex;
    return matrixMultiplication(shape, rotationMatrix)

def rotateAboutYaxis(angle, shape):
    '''
    Pre: angle is the angle to rotate by,
    shape is a matrix of verticies to rotate;
    Purpose: Rotate the veticies about the Y-axis;
    Post: Return the rotated matrix of verticies;
    '''
    theta = math.radians(angle)
    rotationMatrix = [[math.cos(theta), 0, math.sin(theta)],
                      [0, 1, 0],
                      [(-1 * math.sin(theta)), 0, math.cos(theta)]]

    # Perform matrix multiplication for each vertex;
    return matrixMultiplication(shape, rotationMatrix)


def rotateAboutZaxis(angle, shape):
    '''
    Pre: angle is the angle to rotate by,
    shape is a matrix of verticies to rotate;
    Purpose: Rotate the veticies about the Z-axis;
    Post: Return the rotated matrix of verticies;
    '''
    theta = math.radians(angle)
    rotationMatrix = [[math.cos(theta), (-1 * math.sin(theta)), 0],
                      [math.sin(theta), math.cos(theta), 0],
                      [0, 0, 1]]

    # Perform matrix multiplication for each vertex;
    return matrixMultiplication(shape, rotationMatrix)


def convertToIsometric(shape):
    '''
    Pre: shape is a matrix of rotated verticies;
    Purpose: Given a matrix of verticies in R^3
     transform each verticy into an isometric
     representation in R^2;
    Post: Return a matrix of verticies projected in R^2;
    '''
    rotationMatrix = [[math.sqrt(3), 0, (-1 * math.sqrt(3))],
                      [1, 2, 1],
                      [math.sqrt(2), (-1 * math.sqrt(2)), math.sqrt(2)]]
    rotationScalar = (1 / math.sqrt(6))

    projectionMatrix = [[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 0]]

    rotated = matrixMultiplication(shape, rotationMatrix)

    # Scale each coord by 1/sqrt(6);
    for i in range(len(shape)):
        for j in range(3):
            rotated[i][j] = (rotated[i][j] * rotationScalar)
    projection = matrixMultiplication(rotated, projectionMatrix)

    return projection


def matrixMultiplication(shape, standardMatrix):
    '''
    Pre: shape is a matrix of verticies to transform,
    standardMatrix is the matrix to transform shape by
    Purpose: Perform matrix multiplication on a R^3 shape
    and a 3x3 standardMatrix;
    Post: Returns the transformed matrix;
    '''
    rotatedShape = []
    for i in range(len(shape)):
        vertex = shape[i]
        rotatedShape.append(list())
        # For each row in rotationMatrix
        # multiply by each coordinate Vx, Vy, Vz in vertex;
        for j in range(3):
            rotatedShape[i].append((standardMatrix[j][0] * vertex[0]) + (standardMatrix[j][1] * vertex[1]) + (standardMatrix[j][2] * vertex[2]))

    return rotatedShape


def render(shape, height, width, angle):
    '''
    Pre: shape is a matrix of verticies projected from 3D onto
    2D isometrically;
    Purpose connect the verticies by a series of lines;
    '''
    # Rotate the shape
    win = graphPy.GraphWin("Rotating Shape", height, width)
    win.setCoords((-1 * width // 2), (-1 * height // 2), (width // 2), (height // 2))
    colors = ['red', 'blue', 'yellow', 'black', 'pink', 'grey', 'green', 'orange', 'olive', 'cyan', 'khaki', 'teal']
    rotated = rotateIn3D(angle, shape)

    while True:
        points = []
        projected = convertToIsometric(rotated)
        for i in range(len(shape)):
            vertex = projected[i]
            points.append(graphPy.Point(vertex[0], vertex[1]))
            points[i].setFill(choice(colors))

        lines = []
        lines = [graphPy.Line(points[0], points[1]),
                 graphPy.Line(points[0], points[2]),
                 graphPy.Line(points[0], points[4]),
                 graphPy.Line(points[3], points[1]),
                 graphPy.Line(points[3], points[2]),
                 graphPy.Line(points[3], points[7]),
                 graphPy.Line(points[6], points[2]),
                 graphPy.Line(points[6], points[4]),
                 graphPy.Line(points[6], points[7]),
                 graphPy.Line(points[5], points[1]),
                 graphPy.Line(points[5], points[4]),
                 graphPy.Line(points[5], points[7])]

        for i in range(len(lines)):
            lines[i].setFill(colors[i])

        drawLines(points, lines, win)
        sleep(0.4)
        undrawLines(lines, win)

        rotated = rotateIn3D(angle, rotated)

        if win.checkMouse() is not None:
            break

    win.close()


def drawLines(points, lines, win):
    for i in range(len(lines)):
        lines[i].draw(win)


def undrawLines(lines, win):
    for i in range(len(lines)):
        lines[i].undraw()


def main():
    #height = int(input("Enter Window Height: "))
    #width = int(input("Enter Window Width: "))
    #scalar = int(input("Enter Size of the object: "))
    angleX = int(input("Enter Angle to rotate by on the X-axis (degrees): "))
    angleY = int(input("Enter Angle to rotate by on the X-axis (degrees): "))
    angleZ = int(input("Enter Angle to rotate by on the X-axis (degrees): "))

    height = 1000
    width = 1000
    scalar = 100
    # Cube verticies with side length 2;
    cube = [[-1, -1, 1],
            [1, -1, 1],
            [-1, -1, -1],
            [1, -1, -1],
            [-1, 1, 1],
            [1, 1, 1],
            [-1, 1, -1],
            [1, 1, -1]]

    for i in range(len(cube)):
        for j in range(3):
            cube[i][j] = cube[i][j] * scalar

    render(cube, height, width, (angleX, angleY, angleZ))


if __name__ == "__main__":
    main()
