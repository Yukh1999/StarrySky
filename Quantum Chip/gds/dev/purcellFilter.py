import gdspy
from gdspy.library import Cell


def purcellFilter(lineWidth: float, gapWidth: float, straightLength: float, turnRadius: float,
                  turnNum: int, meanderEndLength: float, endLength: float, cell: Cell):
    """
    Purcell Filter

    :param lineWidth: line width
    :param gapWidth: gap width
    :param straightLength: the length of straight line
    :param turnRadius: the radius of turns
    :param turnNum: the number of turns
    :param meanderEndLength: the length of ending part of meander
    :param endLength: the length of ending straight line
    :param cell: cell
    """
    line = gdspy.Path(width=gapWidth, initial_point=[0, 0], number_of_paths=2, distance=lineWidth + gapWidth)

    # Starting straight line
    startLength = turnRadius + lineWidth / 2 + gapWidth + straightLength
    line.segment(length=startLength, direction='-y')

    # Meander
    for i in range(turnNum):
        if i % 2 == 0:
            angle = 'll'
            direction = '+y'
        else:
            angle = 'rr'
            direction = '-y'

        line.turn(radius=turnRadius, angle=angle)
        if i == turnNum - 1:
            # Meander ending part
            line.segment(length=meanderEndLength, direction=direction)
            if direction == '-y':
                line.turn(radius=turnRadius, angle='r')
            else:
                line.turn(radius=turnRadius, angle='l')
        else:
            line.segment(length=straightLength, direction=direction)

    # Ending straight line
    line.segment(length=endLength, direction='-x')

    cell.add(line)


if __name__ == '__main__':
    lib = gdspy.GdsLibrary()
    cell = lib.new_cell('purcellFilter')
    purcellFilter(lineWidth=20, gapWidth=10, straightLength=832, turnRadius=100,
                  turnNum=4, meanderEndLength=1065, endLength=530, cell=cell)
    lib.write_gds('purcellFilter.gds')
    gdspy.LayoutViewer()
