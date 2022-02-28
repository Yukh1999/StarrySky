import gdspy
from gdspy.library import Cell
from typing import List, Dict
import numpy as np

# Access to lib
lib = gdspy.GdsLibrary()

# Line cell
lineCell = lib.new_cell('transLine')


def lineAngle(startCoord: List, endCoord: List):
    """
    The angle between the line connecting the start and end coordinates and the X-axis

    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]

    :return: angle
    """
    yDiff = endCoord[1] - startCoord[1]
    xDiff = endCoord[0] - startCoord[0]
    if xDiff == 0:
        if yDiff > 0:
            theta = np.pi / 2
        else:
            theta = -np.pi / 2
    elif yDiff == 0:
        if xDiff > 0:
            theta = 0
        else:
            theta = np.pi
    else:
        theta = np.arctan(yDiff / xDiff)

    return theta


def straightCpwLine(startCoord: List, endCoord: List, lineWidth: float, gapWidth: float, cell: Cell, layer: int = 0):
    """
    Straight CPW line

    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]
    :param lineWidth: the line width
    :param gapWidth: the gap width
    :param cell: cell
    """
    # The angle between the line and x-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)

    startCoord = np.array(startCoord)
    endCoord = np.array(endCoord)

    # Check input
    lineLength = np.sqrt((endCoord[1] - startCoord[1]) ** 2 + (endCoord[0] - startCoord[0]) ** 2)
    if lineLength == 0:
        raise Exception('Error! Line length is zero!')

    # Params of polar coordinate
    outerRadius = gapWidth + lineWidth / 2
    innerRadius = lineWidth / 2

    # Upper part
    # Coordinates used to draw rectangle of CPW
    upperCoord1 = startCoord + np.array(
        [outerRadius * np.cos(theta + np.pi / 2), outerRadius * np.sin(theta + np.pi / 2)])
    upperCoord2 = startCoord + np.array(
        [innerRadius * np.cos(theta + np.pi / 2), innerRadius * np.sin(theta + np.pi / 2)])
    upperCoord3 = endCoord + np.array(
        [innerRadius * np.cos(theta + np.pi / 2), innerRadius * np.sin(theta + np.pi / 2)])
    upperCoord4 = endCoord + np.array(
        [outerRadius * np.cos(theta + np.pi / 2), outerRadius * np.sin(theta + np.pi / 2)])

    cell.add(gdspy.Polygon([upperCoord1, upperCoord2, upperCoord3, upperCoord4], layer=layer))

    # Lower part
    # Coordinates used to draw rectangle of CPW
    lowerCoord1 = startCoord + np.array(
        [outerRadius * np.cos(theta - np.pi / 2), outerRadius * np.sin(theta - np.pi / 2)])
    lowerCoord2 = startCoord + np.array(
        [innerRadius * np.cos(theta - np.pi / 2), innerRadius * np.sin(theta - np.pi / 2)])
    lowerCoord3 = endCoord + np.array(
        [innerRadius * np.cos(theta - np.pi / 2), innerRadius * np.sin(theta - np.pi / 2)])
    lowerCoord4 = endCoord + np.array(
        [outerRadius * np.cos(theta - np.pi / 2), outerRadius * np.sin(theta - np.pi / 2)])

    cell.add(gdspy.Polygon([lowerCoord1, lowerCoord2, lowerCoord3, lowerCoord4], layer=layer))

    return [[upperCoord1, upperCoord2, upperCoord3, upperCoord4],
            [lowerCoord1, lowerCoord2, lowerCoord3, lowerCoord4]]


def rectAnyDirection(startCoord: List, endCoord: List, rectWidth: float, cell: Cell, layer: int = 0):
    """
    Rectangle in any direction

    :param startCoord: the starting coordinates of the central axis of the rectangle
    :param endCoord: the ending coordinates of the central axis of the rectangle
    :param rectWidth: the width perpendicular to the central axis
    """
    # The angle between the line and the X-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)

    startCoord = np.array(startCoord)
    endCoord = np.array(endCoord)

    coord1 = startCoord + np.array([rectWidth / 2 * np.cos(theta + np.pi / 2),
                                    rectWidth / 2 * np.sin(theta + np.pi / 2)])
    coord2 = startCoord + np.array([rectWidth / 2 * np.cos(theta - np.pi / 2),
                                    rectWidth / 2 * np.sin(theta - np.pi / 2)])
    coord3 = endCoord + np.array([rectWidth / 2 * np.cos(theta - np.pi / 2),
                                  rectWidth / 2 * np.sin(theta - np.pi / 2)])
    coord4 = endCoord + np.array([rectWidth / 2 * np.cos(theta + np.pi / 2),
                                  rectWidth / 2 * np.sin(theta + np.pi / 2)])

    cell.add(gdspy.Polygon([coord1, coord2, coord3, coord4], layer=layer))


def cutOff(startCoord: List, endCoord: List, length: float, width: float, cell: Cell, layer: int = 0):
    """
    Add cut-off zone at the starting and end
    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]
    :param length: length of cut-off zone
    :param width: width of cut-off zone
    """
    # The angle between the line and x-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)

    # Starting part
    startCoord1 = [startCoord[0] - length * np.cos(theta), startCoord[1] - length * np.sin(theta)]
    endCoord1 = startCoord
    rectAnyDirection(startCoord=startCoord1, endCoord=endCoord1, rectWidth=width, cell=cell, layer=layer)

    # Ending part
    startCoord2 = endCoord
    endCoord2 = [endCoord[0] + length * np.cos(theta), endCoord[1] + length * np.sin(theta)]
    rectAnyDirection(startCoord=startCoord2, endCoord=endCoord2, rectWidth=width, cell=cell, layer=layer)


def transLine(startCoord: List, endCoord: List, lineWidth: float, gapWidth: float, cell: Cell):
    """
    Transmission line

    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]
    :param lineWidth: the line width
    :param gapWidth: the gap width
    :param cell: cell
    """
    # Check input
    lineLength = np.sqrt((endCoord[1] - startCoord[1]) ** 2 + (endCoord[0] - startCoord[0]) ** 2)
    if lineLength == 0:
        raise Exception('Error! Line length is zero!')

    # Line layer
    lineCoords = straightCpwLine(startCoord=startCoord, endCoord=endCoord, lineWidth=lineWidth,
                                 gapWidth=gapWidth, cell=cell)

    # Shield layer
    # Part 2
    straightCpwLine(startCoord=startCoord, endCoord=endCoord, lineWidth=24, gapWidth=5, cell=cell, layer=2)

    # Part 3
    rectAnyDirection(startCoord=startCoord, endCoord=endCoord, rectWidth=36, cell=cell, layer=3)

    # Part 4
    rectAnyDirection(startCoord=startCoord, endCoord=endCoord, rectWidth=56, cell=cell, layer=4)

    return lineCoords


def widerTl(startCoord: List, endCoord: List, lineWidth: float, gapWidth: float, widerStartCoord: List,
            widerLineWidth: float, widerGapWidth: float, widerLength: float, transitionLength: float, cell: Cell):
    """
    Transmission line width wider part to couple with purcell filter

    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]
    :param lineWidth: the line width of common part
    :param gapWidth: the gap width of common part
    :param widerStartCoord: the start coordinate of wider part
    :param widerLineWidth: the line width of wider part
    :param widerGapWidth: the gap width of wider part
    :param widerLength: the length of wider part
    :param transitionLength: the length of transition zone connecting common and wider parts
    """

    lineLength = np.sqrt((endCoord[1] - startCoord[1]) ** 2 + (endCoord[0] - startCoord[0]) ** 2)
    if lineLength == 0:
        raise Exception('Error! Line length is zero!')

    startLineLength = np.sqrt((widerStartCoord[1] - startCoord[1]) ** 2
                              + (widerStartCoord[0] - startCoord[0]) ** 2) - transitionLength
    endLineLength = lineLength - startLineLength - widerLength - transitionLength * 2

    # The angle between the line and the X-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)

    # Starting part
    startPartEndCoord = [startCoord[0] + startLineLength * np.cos(theta),
                         startCoord[1] + startLineLength * np.sin(theta)]
    startPartCoords = transLine(startCoord=startCoord, endCoord=startPartEndCoord,
                                lineWidth=lineWidth, gapWidth=gapWidth, cell=cell)

    # Ending part
    endPartStartCoord = [endCoord[0] - endLineLength * np.cos(theta),
                         endCoord[1] - endLineLength * np.sin(theta)]
    endPartCoords = transLine(startCoord=endPartStartCoord, endCoord=endCoord,
                              lineWidth=lineWidth, gapWidth=gapWidth, cell=cell)

    # Wider part
    widerEndCoord = [widerStartCoord[0] + widerLength * np.cos(theta),
                     widerStartCoord[1] + widerLength * np.sin(theta)]
    widerCoords = straightCpwLine(startCoord=widerStartCoord, endCoord=widerEndCoord,
                                  lineWidth=widerLineWidth, gapWidth=widerGapWidth, cell=cell)

    # Transition part
    transitionUpperCoord1 = [startPartCoords[0][2], startPartCoords[0][3], widerCoords[0][0], widerCoords[0][1]]
    transitionLowerCoord1 = [startPartCoords[1][2], startPartCoords[1][3], widerCoords[1][0], widerCoords[1][1]]
    cell.add(gdspy.Polygon(transitionUpperCoord1))
    cell.add(gdspy.Polygon(transitionLowerCoord1))

    transitionUpperCoord2 = [widerCoords[0][2], widerCoords[0][3], endPartCoords[0][0], endPartCoords[0][1]]
    transitionLowerCoord2 = [widerCoords[1][2], widerCoords[1][3], endPartCoords[1][0], endPartCoords[1][1]]
    cell.add(gdspy.Polygon(transitionUpperCoord2))
    cell.add(gdspy.Polygon(transitionLowerCoord2))

    # Cut off zone
    cutOff(startCoord=widerStartCoord, endCoord=widerEndCoord, length=transitionLength, width=56, cell=cell, layer=5)


for i in range(5):
    x1 = 800 * i
    x2 = 800 * (i+1)
    widerTl(startCoord=[x1, 5], endCoord=[x2, 5], lineWidth=4, gapWidth=4, widerStartCoord=[300 + 800*i, 5],
            widerLineWidth=8, widerGapWidth=8, widerLength=30, transitionLength=10, cell=lineCell)

lib.write_gds('tl.gds')
gdspy.LayoutViewer()
