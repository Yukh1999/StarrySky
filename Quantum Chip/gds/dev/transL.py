import gdspy
from gdspy.library import Cell
from typing import List, Union, Iterable, Sequence
import numpy as np


def pointsDistance(pointCoord1: List[float], pointCoord2: List[float]):
    """
    Calculate the distance between two points

    :param pointCoord1: the coordinates of point 1
    :param pointCoord2: the coordinates of point 2

    :return: distance
    """
    distance = np.sqrt((pointCoord1[0] - pointCoord2[0]) ** 2 + (pointCoord1[1] - pointCoord2[1]) ** 2)
    return distance


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


def shield(startCoord: List[float], endCoord: List[float], cell: Cell):
    """
    Shield layer

    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]
    :param cell: Cell object
    """
    # Angle
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)
    # Length
    length = pointsDistance(startCoord, endCoord)
    # Layer 2
    layer2 = gdspy.Path(width=5, initial_point=startCoord, number_of_paths=2, distance=24 + 5)
    layer2.segment(length=length, direction=theta, layer=2)

    # Layer 3
    layer3 = gdspy.Path(width=36, initial_point=startCoord, number_of_paths=1)
    layer3.segment(length=length, direction=theta, layer=3)

    # Layer 4
    layer4 = gdspy.Path(width=56, initial_point=startCoord, number_of_paths=1)
    layer4.segment(length=length, direction=theta, layer=4)

    cell.add([layer2, layer3, layer4])


def cutOff(startCoord: List, endCoord: List, length: float, cell: Cell):
    """
    Add cut-off zone at the starting and end

    :param startCoord: starting coordinate [x, y]
    :param endCoord: ending coordinate [x, y]
    :param length: length of cut-off zone
    :param cell: Cell object
    """
    # Default width
    width = 56
    # The angle between the line and x-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)

    # Starting part
    startCoord1 = [startCoord[0] - length * np.cos(theta), startCoord[1] - length * np.sin(theta)]
    left = gdspy.Path(width=width, initial_point=startCoord1, number_of_paths=1)
    left.segment(length=length, direction=theta, layer=5)

    # Ending part
    startCoord2 = endCoord
    right = gdspy.Path(width=width, initial_point=startCoord2, number_of_paths=1)
    right.segment(length=length, direction=theta, layer=5)

    cell.add([left, right])


def transLine(startCoord: List[float], endCoord: List[float], lineWidth: float, gapWidth: float,
              widerStartPosition: Union[float, List[float]], widerLineWidth: Union[float, List[float]],
              widerGapWidth: Union[float, List[float]], widerLength: Union[float, List[float]],
              transitionLength: float, cell: Cell):
    """
    Transmission line

    :param startCoord: starting coordinates [x, y]
    :param endCoord: ending coordinates [x, y]
    :param lineWidth: the line width of common part
    :param gapWidth: the gap width of common part
    :param widerStartPosition: the starting position of wider parts in line
    :param widerLineWidth: the line width of wider parts
    :param widerGapWidth: the gap width of wider parts
    :param widerLength: the length of wider parts
    :param transitionLength: the length of transition zone connecting common and wider parts
    """
    if isinstance(widerStartPosition, Sequence):
        widerNum = len(widerStartPosition)
    else:
        widerNum = 1
        widerStartPosition = [widerStartPosition]

    # The angle between line and x-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)

    # The start coordinates of wider part
    widerStartCoord = [[startCoord[0] + startPosition * np.cos(theta),
                        startCoord[1] + startPosition * np.sin(theta)]
                       for startPosition in widerStartPosition]

    if isinstance(widerLineWidth, Iterable) is not True:
        widerLineWidth = [widerLineWidth for i in range(widerNum)]

    if isinstance(widerGapWidth, Iterable) is not True:
        widerGapWidth = [widerGapWidth for i in range(widerNum)]

    if isinstance(widerLength, Iterable) is not True:
        widerLength = [widerLength for i in range(widerNum)]

    # Drawing
    line = gdspy.Path(width=gapWidth, initial_point=startCoord, number_of_paths=2, distance=lineWidth + gapWidth)

    # Starting line
    startLength = pointsDistance(startCoord, widerStartCoord[0]) - transitionLength
    startLineEndCoord = [startCoord[0] + startLength * np.cos(theta),
                         startCoord[1] + startLength * np.sin(theta)]
    line.segment(length=startLength, direction=theta)
    shield(startCoord=startCoord, endCoord=startLineEndCoord, cell=cell)

    # Midpiece
    for i in range(widerNum):
        line.segment(length=transitionLength, direction=theta, final_width=widerGapWidth[i],
                     final_distance=widerLineWidth[i] + widerGapWidth[i])
        line.segment(length=widerLength[i], direction=theta)
        line.segment(length=transitionLength, direction=theta, final_width=gapWidth,
                     final_distance=lineWidth + gapWidth)
        widerEndCoord = [widerStartCoord[i][0] + widerLength[i] * np.cos(theta),
                         widerStartCoord[i][1] + widerLength[i] * np.sin(theta)]
        cutOff(startCoord=widerStartCoord[i], endCoord=widerEndCoord, length=transitionLength, cell=cell)

        if i != widerNum - 1:
            commonLineLength = pointsDistance(widerStartCoord[i], widerStartCoord[i + 1]) \
                               - transitionLength * 2 - widerLength[i]
            line.segment(length=commonLineLength, direction=theta)
            commonLineStartCoord = [widerStartCoord[i][0] + (transitionLength + widerLength[i]) * np.cos(theta),
                                    widerStartCoord[i][1] + (transitionLength + widerLength[i]) * np.sin(theta)]
            commonLineEndCoord = [commonLineStartCoord[0] + commonLineLength * np.cos(theta),
                                  commonLineStartCoord[1] + commonLineLength * np.sin(theta)]
            shield(startCoord=commonLineStartCoord, endCoord=commonLineEndCoord, cell=cell)

    # Ending line
    endLength = pointsDistance(widerStartCoord[widerNum - 1], endCoord) - widerLength[widerNum - 1] - transitionLength
    line.segment(length=endLength, direction=theta)
    endLineStartCoord = [endCoord[0] - endLength * np.cos(theta),
                         endCoord[1] - endLength * np.sin(theta)]
    shield(startCoord=endLineStartCoord, endCoord=endCoord, cell=cell)

    cell.add(line)


if __name__ == '__main__':
    widerPosition = [100, 200, 300, 400, 500]
    # Access to lib
    lib = gdspy.GdsLibrary()

    # Line cell
    lineCell = lib.new_cell('transLine')
    transLine(startCoord=[0, 0], endCoord=[1000, 500], lineWidth=4, gapWidth=4, widerStartPosition=widerPosition,
              widerLineWidth=8, widerGapWidth=8, widerLength=30, transitionLength=10, cell=lineCell)
    lib.write_gds('tl.gds')
    gdspy.LayoutViewer()
