import gdspy
from gdspy.library import Cell
from typing import List, Union, Iterable, Sequence, Dict, Any
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


def _lineAirBridge(startInfo: Dict[str, Any], length: Union[int, float]) -> Dict[str, Any]:
    holeLength = 5
    holeDistance = 5
    originPos = startInfo['position']
    startDirection = startInfo['direction']
    if type(startDirection) == str:
        if startDirection == '+x':
            startDirection = 0
        elif startDirection == '+y':
            startDirection = np.pi / 2
        elif startDirection == '-x':
            startDirection = np.pi
        elif startDirection == '-y':
            startDirection = np.pi / 2 * 3
        else:
            raise Exception("Please input startDirection as '+x', '-x', '+y', '-y' or a number.")
    startHoleLength = startInfo['startHoleLength']
    if 'elementList' in startInfo:
        elementList = startInfo['elementList']
    else:
        elementList = list()

    if length >= startHoleLength:
        holeNumber = int((length - startHoleLength) // (holeLength + holeDistance))
        endLength = (length - startHoleLength) % (holeLength + holeDistance)

        if startHoleLength > holeLength:
            pStartInterval = gdspy.Path(width=5, initial_point=originPos, number_of_paths=2, distance=32)
            pStartInterval.segment(length=(startHoleLength - holeLength), direction=startDirection, layer=3)
            endPos = [pStartInterval.x, pStartInterval.y]
            pStartHole = gdspy.Path(width=5, initial_point=endPos, number_of_paths=2, distance=32)
            pStartHole.segment(length=holeLength, direction=startDirection, layer=3)

        else:
            pStartHole = gdspy.Path(width=5, initial_point=originPos, number_of_paths=2, distance=32)
            pStartHole.segment(length=startHoleLength, direction=startDirection, layer=3)

        elementList.append(pStartHole)
        endPos = [pStartHole.x, pStartHole.y]

        intervalList = list()
        holeList = list()
        for i in range(holeNumber):
            intervalList.append(gdspy.Path(width=5, initial_point=endPos, number_of_paths=2, distance=32))
            intervalList[i].segment(length=holeDistance, direction=startDirection, layer=3)
            endPos = [intervalList[i].x, intervalList[i].y]
            holeList.append(gdspy.Path(width=5, initial_point=endPos, number_of_paths=2, distance=32))
            holeList[i].segment(length=holeLength, direction=startDirection, layer=3)
            endPos = [holeList[i].x, holeList[i].y]
        elementList.extend(holeList)

    else:
        endLength = length
        endPos = originPos

    if endLength > holeDistance:
        pEndInterval = gdspy.Path(width=5, initial_point=endPos, number_of_paths=2, distance=32)
        pEndInterval.segment(length=holeDistance, direction=startDirection, layer=3)
        endPos = [pEndInterval.x, pEndInterval.y]
        pEndHole = gdspy.Path(width=5, initial_point=endPos, number_of_paths=2, distance=32)
        pEndHole.segment(length=(endLength - holeDistance), direction=startDirection, layer=3)
        endPos = [pEndHole.x, pEndHole.y]
        elementList.append(pEndHole)
    else:
        pEndInterval = gdspy.Path(width=5, initial_point=endPos, number_of_paths=2, distance=32)
        pEndInterval.segment(length=endLength, direction=startDirection, layer=3)
        endPos = [pEndInterval.x, pEndInterval.y]

    nextHoleLength = holeLength + holeDistance - endLength
    endInfo = {'position': endPos, 'direction': startDirection,
               'startHoleLength': nextHoleLength, 'elementList': elementList}

    return endInfo


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
    layer2 = gdspy.Path(width=5, initial_point=startCoord, number_of_paths=2, distance=32)
    layer2.segment(length=length, direction=theta, layer=2)

    # Layer 1
    layer3 = gdspy.Path(width=39, initial_point=startCoord, number_of_paths=1)
    layer3.segment(length=length, direction=theta, layer=1)

    # Layer 0
    layer0 = gdspy.Path(width=56, initial_point=startCoord, number_of_paths=1)
    layer0.segment(length=length, direction=theta, layer=0)

    # Layer 3
    startInfo = {
        'position': startCoord,
        'direction': theta,
        'startHoleLength': 5,
    }
    elementLs = _lineAirBridge(startInfo=startInfo, length=length)['elementList']
    cell.add(elementLs)

    cell.add([layer2, layer3, layer0])


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


def toAnsysCoord(coord: List[float]):
    return [coord[1], -coord[0]]


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
    :param widerStartPosition: the distance between starting position of wider parts and starting
    :param widerLineWidth: the line width of wider parts
    :param widerGapWidth: the gap width of wider parts
    :param widerLength: the length of wider parts
    :param transitionLength: the length of transition zone connecting common and wider parts
    """
    # Transform to ansys coordinate
    startCoordAnsys = toAnsysCoord(startCoord)
    endCoordAnsys = toAnsysCoord(endCoord)

    if isinstance(widerStartPosition, Sequence):
        widerNum = len(widerStartPosition)
    else:
        widerNum = 1
        widerStartPosition = [widerStartPosition]

    # The angle between line and x-axis
    theta = lineAngle(startCoord=startCoord, endCoord=endCoord)
    thetaAnsys = lineAngle(startCoordAnsys, endCoordAnsys)

    # The start coordinates of wider part
    widerStartCoord = [[startCoord[0] + startPosition * np.cos(theta),
                        startCoord[1] + startPosition * np.sin(theta)]
                       for startPosition in widerStartPosition]

    widerStartCoordAnsys = [toAnsysCoord(widerCoord) for widerCoord in widerStartCoord]

    if isinstance(widerLineWidth, Iterable) is not True:
        widerLineWidth = [widerLineWidth for i in range(widerNum)]

    if isinstance(widerGapWidth, Iterable) is not True:
        widerGapWidth = [widerGapWidth for i in range(widerNum)]

    if isinstance(widerLength, Iterable) is not True:
        widerLength = [widerLength for i in range(widerNum)]

    # Drawing
    line = gdspy.Path(width=gapWidth, initial_point=startCoordAnsys, number_of_paths=2, distance=lineWidth + gapWidth)

    # Starting line
    startLength = pointsDistance(startCoord, widerStartCoord[0]) - transitionLength
    startLineEndCoord = [startCoord[0] + startLength * np.cos(theta),
                         startCoord[1] + startLength * np.sin(theta)]
    startLineEndCoordAnsys = toAnsysCoord(startLineEndCoord)
    line.segment(length=startLength, direction=thetaAnsys, layer=4)
    shield(startCoord=startCoordAnsys, endCoord=startLineEndCoordAnsys, cell=cell)

    # Midpiece
    for i in range(widerNum):
        line.segment(length=transitionLength, direction=thetaAnsys, final_width=widerGapWidth[i],
                     final_distance=widerLineWidth[i] + widerGapWidth[i], layer=4)
        line.segment(length=widerLength[i], direction=thetaAnsys, layer=4)
        line.segment(length=transitionLength, direction=thetaAnsys, final_width=gapWidth,
                     final_distance=lineWidth + gapWidth, layer=4)
        widerEndCoord = [widerStartCoord[i][0] + widerLength[i] * np.cos(theta),
                         widerStartCoord[i][1] + widerLength[i] * np.sin(theta)]
        widerEndCoordAnsys = toAnsysCoord(widerEndCoord)
        cutOff(startCoord=widerStartCoordAnsys[i], endCoord=widerEndCoordAnsys, length=transitionLength, cell=cell)

        if i != widerNum - 1:
            commonLineLength = pointsDistance(widerStartCoord[i], widerStartCoord[i + 1]) \
                               - transitionLength * 2 - widerLength[i]
            line.segment(length=commonLineLength, direction=thetaAnsys, layer=4)
            commonLineStartCoord = [widerStartCoord[i][0] + (transitionLength + widerLength[i]) * np.cos(theta),
                                    widerStartCoord[i][1] + (transitionLength + widerLength[i]) * np.sin(theta)]
            commonLineEndCoord = [commonLineStartCoord[0] + commonLineLength * np.cos(theta),
                                  commonLineStartCoord[1] + commonLineLength * np.sin(theta)]
            shield(startCoord=toAnsysCoord(commonLineStartCoord), endCoord=toAnsysCoord(commonLineEndCoord), cell=cell)

    # Ending line
    endLength = pointsDistance(widerStartCoord[widerNum - 1], endCoord) - widerLength[widerNum - 1] - transitionLength
    line.segment(length=endLength, direction=thetaAnsys, layer=4)
    endLineStartCoord = [endCoord[0] - endLength * np.cos(theta),
                         endCoord[1] - endLength * np.sin(theta)]
    shield(startCoord=toAnsysCoord(endLineStartCoord), endCoord=toAnsysCoord(endCoord), cell=cell)

    cell.add(line)


if __name__ == '__main__':
    widerPosition = [-1920 + i * 2800 + 3600 for i in range(5)]
    # Access to lib
    lib = gdspy.GdsLibrary()

    # Line cell
    lineCell = lib.new_cell('transLine')

    for row in range(5):
        readoutLeft = [-300 + 2800 * row, -3600]
        readoutRight = [-300 + 2800 * row, 13200]
        transLine(readoutLeft, readoutRight, 5, 5, [-1920 + i * 2800 + 3600 for i in range(5)],
                  20, 10, 1400, 100, lineCell)

    lib.write_gds('tl.gds')
    gdspy.LayoutViewer()
