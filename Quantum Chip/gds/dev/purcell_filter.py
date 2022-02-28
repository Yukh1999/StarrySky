import gdspy
import numpy as np
from gdspy.library import Cell


def purcellFilter(lineWidth: float, gapWidth: float, lineStraight: float, arcOuterRadius: float,
                  endLineLength: float, cell: Cell):
    """
    Purcell Filter

    :param lineWidth: line width
    :param gapWidth: gap width
    :param lineStraight: the length of straight part
    :param arcOuterRadius: the outer radius of arc
    :param endLineLength: the length of ending part of line
    """

    arcInnerRadius = arcOuterRadius - gapWidth * 2 - lineWidth

    lineInterval = arcOuterRadius * 2 - (lineWidth + gapWidth * 2)

    # Straight line
    # Starting
    rect1 = gdspy.Rectangle((0, 0), (gapWidth, -lineStraight - arcOuterRadius))
    rect2 = gdspy.Rectangle((gapWidth + lineWidth, 0), (gapWidth * 2 + lineWidth, -lineStraight - arcOuterRadius))
    cell.add(rect1)
    cell.add(rect2)

    # Meander
    for i in range(1, 4):
        rectLeft = gdspy.Rectangle((lineInterval * i, -arcOuterRadius),
                                   (lineInterval * i + gapWidth, -lineStraight - arcOuterRadius))
        rectRight = gdspy.Rectangle((lineInterval * i + gapWidth + lineWidth, -arcOuterRadius),
                                    (lineInterval * i + gapWidth * 2 + lineWidth, -lineStraight - arcOuterRadius))
        cell.add(rectLeft)
        cell.add(rectRight)
    # Meander end
    meanderEndLen = 1065
    rect1 = gdspy.Rectangle((lineInterval * 4, -arcOuterRadius),
                            (lineInterval * 4 + gapWidth, -meanderEndLen - arcOuterRadius))
    rect2 = gdspy.Rectangle((lineInterval * 4 + gapWidth + lineWidth, -arcOuterRadius),
                            (lineInterval * 4 + gapWidth * 2 + lineWidth, -meanderEndLen - arcOuterRadius))
    cell.add(rect1)
    cell.add(rect2)

    # Arc line
    # Meander arc
    for i in range(4):
        if i % 2 == 0:
            centerVertical = -lineStraight - arcOuterRadius
            finalAngle = 2 * np.pi
        else:
            centerVertical = -arcOuterRadius
            finalAngle = 0
        arcInner = gdspy.Round(
            center=(arcOuterRadius + lineInterval * i, centerVertical),
            radius=arcInnerRadius + gapWidth,
            inner_radius=arcInnerRadius,
            initial_angle=np.pi,
            final_angle=finalAngle,
            tolerance=0.01)
        arcOuter = gdspy.Round(
            center=(arcOuterRadius + lineInterval * i, centerVertical),
            radius=arcOuterRadius,
            inner_radius=arcOuterRadius - gapWidth,
            initial_angle=np.pi,
            final_angle=finalAngle,
            tolerance=0.01)
        cell.add(arcInner)
        cell.add(arcOuter)
    # End arc
    arcEndInner = gdspy.Round(
        center=(arcOuterRadius + lineInterval * 3, -arcOuterRadius - meanderEndLen),
        radius=arcInnerRadius + gapWidth,
        inner_radius=arcInnerRadius,
        initial_angle=0,
        final_angle=-np.pi / 2,
        tolerance=0.01)
    arcEndOuter = gdspy.Round(
        center=(arcOuterRadius + lineInterval * 3, -arcOuterRadius - meanderEndLen),
        radius=arcOuterRadius,
        inner_radius=arcOuterRadius - gapWidth,
        initial_angle=0,
        final_angle=-np.pi / 2,
        tolerance=0.01)
    cell.add([arcEndOuter, arcEndInner])

    # End line
    rect1 = gdspy.Rectangle((arcOuterRadius + lineInterval * 3, -arcOuterRadius - meanderEndLen - arcInnerRadius),
                            (arcOuterRadius + lineInterval * 3 - endLineLength,
                             -arcOuterRadius - meanderEndLen - arcInnerRadius - gapWidth))
    rect2 = gdspy.Rectangle((arcOuterRadius + lineInterval * 3,
                             -arcOuterRadius - meanderEndLen - arcInnerRadius - gapWidth - lineWidth),
                            (arcOuterRadius + lineInterval * 3 - endLineLength,
                             -arcOuterRadius - meanderEndLen - arcInnerRadius - gapWidth * 2 - lineWidth))
    cell.add([rect1, rect2])

if __name__ == '__main__':

    # Access to lib
    lib = gdspy.GdsLibrary()

    # Line cell
    cell = lib.new_cell('purcellFilter')
    purcellFilter(lineWidth=20, gapWidth=10, lineStraight=832, arcOuterRadius=120,
                  endLineLength=530, cell=cell)

    # Write gds
    lib.write_gds('purcell.gds')

    # View
    gdspy.LayoutViewer()
