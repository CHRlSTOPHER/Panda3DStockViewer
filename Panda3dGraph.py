from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs
from direct.interval.IntervalGlobal import Sequence, Func, Wait

from StockViewer.StockScrapper import StockScrapper
import StockGlobals as SG


class Panda3dGraph(ShowBase, StockScrapper):

    def __init__(self):
        ShowBase.__init__(self)
        StockScrapper.__init__(self)
        self.graph = None
        self.line_seg = None
        self.draw_sequence = Sequence()

        self.generate_graph()

    def generate_graph(self):
        line_collection = self.create_lines()

        self.draw_sequence.append(Wait(1))
        for geom_node in line_collection:
            self.draw_sequence.append(Wait(.03))
            self.draw_sequence.append(Func(self.render_line, geom_node))
        self.draw_sequence.start()

    def create_lines(self):
        line_seg = LineSegs()
        line_seg.set_color(1, 0, 0, 1)
        line_seg.set_thickness(SG.LINE_THICKNESS)

        line_collection = []
        i = 0
        last_pos = None
        for point in self.graph_points:
            x_point = i
            if point:
                # determine z value based on max high and the ratio
                z_point = point / self.high * SG.Z_RATIO
                # move pointer to next point
                if last_pos:
                    line_seg.move_to(last_pos)
                line_seg.draw_to(x_point, 0, z_point)
                line = line_seg.create()
                last_pos = (x_point, 0, z_point)
                line_collection.append(line)
            i += 1
        return line_collection

    def render_line(self, geom_node):
        graph_node = self.render.attach_new_node(geom_node)
        graph_node.set_pos(-10, 25, -SG.Z_RATIO + 5.0)
        graph_node.set_scale(.05, 1, 1)


scene = Panda3dGraph()
scene.oobe()
scene.camera.hide()
scene.run()
