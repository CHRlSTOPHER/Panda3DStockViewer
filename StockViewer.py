"""View up to 6 live stock graphs (while market is active ofc)
   If market is not active, the last active period will be shown."""
import json
import requests

from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import loadPrcFileData

from StockGraph import StockGraph, get_crumb
import StockGlobals as SG

loadPrcFileData("", f"win-size {SG.WIN_SIZE}")
loadPrcFileData('', 'win-fixed-size 1')

# put stocks here since user may want to switch them out daily.
STOCKS = [
    ('NVDA', 891.25),
    ("SMCI", 765.40),
    ("MSFT", None),
    ("GFAI", None),
    ("MSCI", None),
    ("QUBT", None),
]
# Up to 6 stocks can be drawn
STOCKS = STOCKS[:6]


class StockViewer(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.crumb = None
        self.cookie = None
        self.stock_graphs = {}
        self.refresh_period = len(STOCKS)

        # put a short interval between each graph creation
        # to avoid spamming the server
        self.generate_sequence = Sequence()
        self.generate()
        self.generate_sequence.start()

    def generate(self):
        # get the crumb and cookie from yahoo finance
        self.crumb, self.cookie = get_crumb()

        i = 0
        for stock, investment in STOCKS:
            self.generate_sequence.append(Func(self.create_stock_graph,
                                               stock, investment))
            self.generate_sequence.append((Func(self.adjust_graph, stock, i)))
            self.generate_sequence.append(Wait(SG.PAUSE_DURATION))
            i += 1

    def create_stock_graph(self, stock_name, investment):
        stock_graph = StockGraph(self, stock_name, investment,
                                 self.crumb, self.cookie)
        stock_graph.scrape_stock_data()
        stock_graph.generate_graph()
        self.stock_graphs[stock_name] = stock_graph
        # refresh once every x amount of seconds. based on number of stocks.
        self.taskMgr.doMethodLater(self.refresh_period, self.refresh_graph,
                                   f"{stock_name}")

    def adjust_graph(self, stock_name, i):
        graph = self.stock_graphs[stock_name]
        graph.set_pos(SG.GRAPH_POSITIONS[i])
        graph.set_scale(SG.GRAPH_SCALE)

    def refresh_graph(self, task):
        graph = self.stock_graphs[task.get_name()]
        graph.update()
        if graph.end_of_day:
            return task.done  # market hours are over.
        return task.again


stock_viewer = StockViewer()
stock_viewer.disable_mouse()
stock_viewer.camera.set_pos(1.75, -32, 0)
stock_viewer.run()
