import gdspy

lib = gdspy.GdsLibrary()
cell = lib.new_cell('First')

# Rect
rect = gdspy.Rectangle((0, 0), (2, 3))
cell.add(rect)

# Polygon
points = [(0, 0), (2, 3), (7, 2), (15, 15)]
polygon = gdspy.Polygon(points=points)
cell2 = lib.new_cell('Second')
cell2.add(polygon)

# Circles


gdspy.LayoutViewer()
