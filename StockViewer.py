"""View stock graphs (while market is active ofc)
   If market is not active, the last active period will be shown."""
import json

from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import loadPrcFileData

from StockGraph import StockGraph, get_crumb
import StockGlobals as SG

loadPrcFileData("", f"win-size {SG.WIN_SIZE}")
loadPrcFileData('', 'win-fixed-size 1')

STOCKS = json.loads(open(SG.STOCK_JSON).read())


class StockViewer(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.crumb = None
        self.cookie = None
        self.stock_graphs = {}
        self.stock_graphs_list = []
        self.refresh_sequences = {}
        self.refresh_period = len(STOCKS)
        self.end_of_day = False

        # put a short interval between each graph creation
        # to avoid spamming the server
        self.generate_sequence = Sequence()
        self.generate()
        self.generate_sequence.start()

    def generate(self):
        # get the crumb and cookie from yahoo finance
        self.crumb, self.cookie = get_crumb()

        i = 0
        for stock in STOCKS:
            if i >= SG.STOCK_LIMIT:  # limit the amount of graphs.
                break
            investment = STOCKS.get(stock)
            self.stock_graphs_list.append(stock)
            self.generate_sequence.append(Func(self.create_stock_graph,
                                               stock, investment, len(STOCKS)))
            self.generate_sequence.append((Func(self.adjust_graph, stock, i)))
            self.generate_sequence.append(Wait(SG.PAUSE_DURATION))
            i += 1

    def create_stock_graph(self, stock_name, investment, stock_len):
        stock_graph = StockGraph(self, stock_name, investment, stock_len,
                                 self.crumb, self.cookie)
        graph_data = stock_graph.scrape_stock_data()
        if not graph_data:
            return  # data not found. abort.
        stock_graph.generate_graph()
        self.stock_graphs[stock_name] = stock_graph

        # refresh once every x amount of seconds. based on number of stocks.
        refresh_sequence = Sequence()
        refresh_sequence.append(Func(self.refresh_graph, stock_name))
        refresh_sequence.append(Wait(self.refresh_period))
        refresh_sequence.loop()
        self.refresh_sequences[stock_name] = refresh_sequence

    def adjust_graph(self, stock_name, i):
        graph = self.stock_graphs.get(stock_name)
        if graph:
            graph.set_pos(SG.GRAPH_POSITIONS[i])
            graph.set_scale(SG.GRAPH_SCALE)

    def refresh_graph(self, stock_name):
        graph = self.stock_graphs[stock_name]
        graph.update()
        index = self.stock_graphs_list.index(stock_name)
        graph.set_pos(SG.GRAPH_POSITIONS[index])
        graph.set_scale(SG.GRAPH_SCALE)
        if graph.end_of_day:
            # occasionally chart data will not return the proper market end
            # time, making the code believe the market is still active.
            # so as long as one graph says it is end of day,
            # then we can assume it is end of day for all.
            self.end_of_day = True
        if self.end_of_day:
            self.refresh_sequences[stock_name].finish()


stock_viewer = StockViewer()
stock_viewer.disable_mouse()
stock_viewer.camera.set_pos(1, -60, -.7)
stock_viewer.run()
