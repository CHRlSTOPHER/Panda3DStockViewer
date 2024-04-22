from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs

from StockViewer.StockScrapper import StockScrapper
import StockGlobals as SG


class Panda3dGraph(ShowBase, StockScrapper):

    def __init__(self):
        ShowBase.__init__(self)
        StockScrapper.__init__(self)
        self.graph = None
        self.line_seg = None
        self.draw_graph()

    def draw_graph(self):
        self.line_seg = LineSegs()
        self.line_seg.set_color(1, 0, 0, 1)
        self.line_seg.set_thickness(SG.LINE_THICKNESS)
        i = 0
        for point in self.graph_points:
            # determine x value based on market duration
            x_point = (i / SG.MARKET_DURATION) * SG.X_MULTIPLIER
            # determine z value based on max high and the ratio
            z_point = point / self.high * SG.Z_RATIO
            # move pointer to next point
            self.line_seg.draw_to(x_point, 0, z_point)
            i += 1
        self.line_graph = self.line_seg.create()
        self.graph_node = self.render.attach_new_node(self.line_graph)
        self.graph_node.set_z(-SG.Z_RATIO)


scene = Panda3dGraph()
scene.oobe()
scene.camera.hide()
scene.run()
