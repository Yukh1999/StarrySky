import gdspy
import numpy as np

# Parameters
lineInfo = {
    'lineWidth': 20,
    'gapWidth': 10
}
lineWidth = lineInfo['lineWidth']
gapWidth = lineInfo['gapWidth']

lineStraight = 832

arcOuterRadius = 120
arcInnerRadius = arcOuterRadius - gapWidth*2 - lineWidth

lineInterval = arcOuterRadius * 2 - (lineWidth + gapWidth * 2)

# Access to lib
lib = gdspy.GdsLibrary()

# Line cell
cell = lib.new_cell('line')
# Straight line
# Starting
rect1 = gdspy.Rectangle((0, 0), (gapWidth, -lineStraight-arcOuterRadius))
rect2 = gdspy.Rectangle((gapWidth + lineWidth, 0), (gapWidth*2 + lineWidth, -lineStraight-arcOuterRadius))
cell.add(rect1)
cell.add(rect2)

# Meander
for i in range(1, 4):
    rectLeft = gdspy.Rectangle((lineInterval * i, -arcOuterRadius),
                               (lineInterval * i + gapWidth, -lineStraight - arcOuterRadius))
    rectRight = gdspy.Rectangle((lineInterval * i + gapWidth + lineWidth, -arcOuterRadius),
                                (lineInterval * i + gapWidth*2 + lineWidth, -lineStraight - arcOuterRadius))
    cell.add(rectLeft)
    cell.add(rectRight)
# Meander end
meanderEndLen = 1065
rect1 = gdspy.Rectangle((lineInterval * 4, -arcOuterRadius),
                        (lineInterval * 4 + gapWidth, -meanderEndLen - arcOuterRadius))
rect2 = gdspy.Rectangle((lineInterval * 4 + gapWidth + lineWidth, -arcOuterRadius),
                        (lineInterval * 4 + gapWidth*2 + lineWidth, -meanderEndLen - arcOuterRadius))
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
        final_angle=-np.pi/2,
        tolerance=0.01)
arcEndOuter = gdspy.Round(
        center=(arcOuterRadius + lineInterval * 3, -arcOuterRadius - meanderEndLen),
        radius=arcOuterRadius,
        inner_radius=arcOuterRadius - gapWidth,
        initial_angle=0,
        final_angle=-np.pi/2,
        tolerance=0.01)
cell.add([arcEndOuter, arcEndInner])

# End line
endLineLen = 530
rect1 = gdspy.Rectangle((arcOuterRadius + lineInterval * 3, -arcOuterRadius - meanderEndLen - arcInnerRadius),
                        (arcOuterRadius + lineInterval * 3 - endLineLen,
                         -arcOuterRadius - meanderEndLen - arcInnerRadius - gapWidth))
rect2 = gdspy.Rectangle((arcOuterRadius + lineInterval * 3,
                         -arcOuterRadius - meanderEndLen - arcInnerRadius - gapWidth - lineWidth),
                        (arcOuterRadius + lineInterval * 3 - endLineLen,
                         -arcOuterRadius - meanderEndLen - arcInnerRadius - gapWidth*2 - lineWidth))
cell.add([rect1, rect2])


# Write gds
lib.write_gds('purcell.gds')

# View
gdspy.LayoutViewer()
