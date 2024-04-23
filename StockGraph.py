import requests
import math

from panda3d.core import LineSegs, NodePath, TextNode
from direct.interval.IntervalGlobal import Sequence, Func, Wait

import StockGlobals as SG


class StockGraph(NodePath):

    def __init__(self, showbase, stock_name, crumb, cookie):
        NodePath.__init__(self, "stock_graph")
        self.showbase = showbase
        self.chart_data = None
        self.stock_name = stock_name
        self.crumb = crumb
        self.cookie = cookie
        self.graph = None
        self.line_seg = None
        self.market_price = None
        self.company_data = None
        self.graph_points = None
        self.last_minute = None
        self.low = 0
        self.high = 0
        self.price_text_node = None
        self.draw_sequence = Sequence()

    def scrape_stock_data(self):
        # we define this to determine the past graph points
        self.chart_data = self.get_chart_data()
        result = self.chart_data["chart"]["result"][0]
        self.graph_points = result['indicators']['quote'][0]['close']
        self.low, self.high = self.get_low_and_high_price()

    def generate_graph(self, wait=.01):
        line_collection = self.create_lines()

        self.draw_sequence.append(Wait(.1))
        for geom_node in line_collection:
            self.draw_sequence.append(Wait(wait))
            self.draw_sequence.append(Func(self.render_line, geom_node))
        self.draw_sequence.start()

        self.generate_company_text()
        self.generate_price_text()

    def create_lines(self):
        self.line_seg = LineSegs()
        self.line_seg.set_color(1, 0, 0, 1)
        self.line_seg.set_thickness(SG.LINE_THICKNESS)

        line_collection = []
        self.x = 0
        self.last_pos = None
        self.point = None
        for point in self.graph_points:
            # store this in the class for later use.
            self.point = point
            x_point = self.x
            if self.point:
                # determine z value based on max high and the ratio
                z_point = self.point / self.high * SG.Z_RATIO
                # move pointer to next point
                if self.last_pos:
                    self.line_seg.move_to(self.last_pos)
                self.line_seg.draw_to(x_point, 0, z_point)
                line = self.line_seg.create()
                self.last_pos = (x_point, 0, z_point)
                line_collection.append(line)
            self.x += 1
        return line_collection

    def render_line(self, geom_node):
        graph_node = self.attach_new_node(geom_node)
        graph_node.set_pos(-10, 0, -SG.Z_RATIO + 5.0)
        graph_node.set_scale(.05, 1, 1)
        self.reparent_to(self.showbase.render)

    def update(self):
        company_data = self.get_company_data()
        result = company_data["quoteSummary"]["result"][0]
        market_time = result["price"]["regularMarketTime"]
        minutes = math.floor(market_time / 60)
        market_price = result["price"]["regularMarketPrice"]["raw"]

        # check if last_minute has been defined
        if not self.last_minute:
            self.last_minute = minutes

        # check if it has been a minute since the last update
        if minutes != self.last_minute:
            # add a new line if so
            self.append_new_line(minutes, market_price)
            # update minute
            self.last_minute = minutes

        # update the price text
        self.update_price_text(market_price)

        print(f"{self.stock_name}: EPOCH: {math.floor(market_time / 60)},"
              f" ${market_price}")

    def generate_company_text(self):
        self.stock_text = TextNode("stock_text")
        self.stock_text.set_text(self.stock_name)
        self.stock_text.set_shadow(0.05, 0.05)
        self.stock_text_node = self.attach_new_node(self.stock_text)
        self.stock_text_node.set_pos(SG.STOCK_POS)
        self.stock_text_node.set_scale(SG.STOCK_SCALE)
        self.stock_text_node.set_depth_write(0)

    def generate_price_text(self):
        self.price_text = TextNode("price_text")
        string_price = str(math.floor(self.point * 100)/100.0)
        self.price_text.set_text(string_price)
        self.price_text.set_shadow(0.05, 0.05)
        self.price_text_node = self.attach_new_node(self.price_text)
        self.price_text_node.set_pos(SG.TEXT_POS)
        self.price_text_node.set_scale(SG.TEXT_SCALE)
        self.price_text_node.set_depth_write(0)

    def update_price_text(self, price):
        string_price = str(math.floor(price * 100)/100.0)
        self.price_text.set_text(string_price)

    def append_new_line(self, time, price):
        self.line_seg.set_color(0, 1, 0, 1)
        # add the new value to the graph
        x_point = self.x
        # determine z value based on max high and the ratio
        z_point = price / self.high * SG.Z_RATIO
        # move pointer to next point
        if self.last_pos:
            self.line_seg.move_to(self.last_pos)
        self.line_seg.draw_to(x_point, 0, z_point)
        line = self.line_seg.create()
        self.render_line(line)
        self.last_pos = (x_point, 0, z_point)
        self.x += 1

    def get_chart_data(self):
        chart_data = requests.get(f"{SG.FINANCE_URL}{SG.CHART_DATA}"
                                  f"{self.stock_name}",
                                  params={"interval": "1m",
                                          "range": "1d",
                                          "includePrePost": "false"},
                                  headers={'user-agent': SG.USER_AGENT,
                                           'cookie': self.cookie})
        return chart_data.json()

    def get_company_data(self, asset_profile=False):
        modules = "price"
        if asset_profile:
            modules = "price,assetProfile"
        company_data = requests.get(f"{SG.FINANCE_URL}{SG.COMPANY_DATA}"
                                    f"{self.stock_name}",
                                    params={'modules': modules,
                                            "crumb": self.crumb},
                                    headers={'user-agent': SG.USER_AGENT,
                                             'cookie': self.cookie})
        return company_data.json()

    def get_low_and_high_price(self):
        valid_points = []
        for point in self.graph_points:
            if point:
                valid_points.append(point)
        return min(*valid_points), max(*valid_points)
