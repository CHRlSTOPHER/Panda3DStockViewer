import requests
import math

from panda3d.core import LineSegs, NodePath
from direct.interval.IntervalGlobal import Sequence, Func, Wait

from StockTextNodes import StockTextNodes
import StockGlobals as SG


def get_crumb():
    request = requests.get(SG.YAHOO_FINANCE_WEBSITE)
    cookie_data = request.headers['set-cookie']
    cookie = cookie_data.split(";")[0]
    request = requests.get(SG.FINANCE_URL + SG.CRUMB,
                           headers={'user-agent': SG.USER_AGENT,
                                    'cookie': cookie})
    return request.text, cookie


class StockGraph(NodePath, StockTextNodes):

    def __init__(self, showbase, stock_name, investment, stock_len,
                 crumb, cookie):
        NodePath.__init__(self, "stock_graph")
        StockTextNodes.__init__(self, stock_name, self)
        self.showbase = showbase
        self.stock_name = stock_name
        self.investment = investment
        self.stock_len = stock_len
        self.crumb = crumb
        self.cookie = cookie
        self.chart_data = None
        self.end_time = None
        self.previous_close = None
        self.graph_points = None
        self.high = 0
        self.low = 0
        self.line_seg = None
        self.last_pos = None
        self.x = None
        self.point = None
        self.graph = None
        self.market_price = None
        self.company_data = None
        self.last_minute = None
        self.last_price = 0
        self.ratio = None
        self.graph_nodes = []
        self.end_of_day = False
        self.draw_sequence = Sequence()

    def scrape_stock_data(self, get_limits=True):
        # we define this to determine the past graph points
        self.chart_data = self.get_chart_data()
        if self.chart_data['chart']['result'] is None:
            print(f"{self.stock_name} not found.")
            return False
        result = self.chart_data["chart"]["result"][0]
        self.end_time = result["meta"][SG.TRADE_PERIOD]["regular"]["end"]
        self.previous_close = result["meta"]["previousClose"]
        del self.graph_points
        self.graph_points = result['indicators']['quote'][0]['close']
        if get_limits:
            self.low, self.high = self.get_low_and_high_price()
            self.high = math.floor(self.high * 100) / 100.0
            self.low = math.floor(self.low * 100) / 100.0
        self.previous_close = math.floor(self.previous_close * 100) / 100
        return True

    def generate_graph(self, wait=.01):
        line_collection = self.create_stock_lines()
        self.create_bg_graph()

        self.draw_sequence.append(Wait(.1))
        for geom_node in line_collection:
            self.draw_sequence.append(Wait(wait))
            self.draw_sequence.append(Func(self.render_line, geom_node))
        self.draw_sequence.start()

        self.generate_company_text()
        self.generate_price_text(self.point)
        self.generate_limits_text(self.high, self.low, self.previous_close)
        if self.investment:
            self.generate_investment_comparison(self.investment, self.point)

    def create_stock_lines(self):
        self.cleanup_graph()
        self.line_seg = LineSegs()
        self.line_seg.set_color(*SG.RED)
        self.line_seg.set_thickness(SG.LINE_THICKNESS)

        line_collection = []
        self.x = 0
        self.last_pos = None
        self.point = self.graph_points[0]
        for point in self.graph_points:
            # store this in the class for later use.
            x_point = self.x
            if point:
                self.point = point
                # get the amount between high and low
                max_difference = self.high - self.low
                current_difference = self.high - self.point
                # divide to get the ratio between 0 and 1 for the graph
                # the point on the graph lies
                self.ratio = current_difference / max_difference
                # make the value lie between 0.5 and 1
                z_point = (self.ratio / 2.0) + 0.5
                # apply multiplier
                z_point *= SG.Z_MULTIPLIER
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
        graph_node.set_pos(-10, 0, 18)
        graph_node.set_scale(SG.GRAPH_SX, 1, SG.GRAPH_SZ)
        self.graph_nodes.append(graph_node)
        self.reparent_to(self.showbase.render)

    def create_bg_graph(self):
        self.bg_line = LineSegs()
        self.bg_line.set_color(*SG.BG_LINE_COLOR)
        self.bg_line.set_thickness(SG.LINE_THICKNESS)
        # draw base line
        self.bg_line.move_to(SG.BG_LINE_POS[0])
        self.bg_line.draw_to(SG.BG_LINE_POS[1])
        self.bg_line.move_to(SG.BG_LINE_POS[2])
        self.bg_line.draw_to(SG.BG_LINE_POS[3])
        self.bg_line_geom = self.bg_line.create()
        self.bg_line_node = self.attach_new_node(self.bg_line_geom)

    def update(self):
        company_data = self.get_company_data()
        result = company_data["quoteSummary"]["result"][0]
        market_time = result["price"]["regularMarketTime"]
        minutes = math.floor(market_time / 60)
        market_price = result["price"]["regularMarketPrice"]["raw"]
        market_price = math.floor(market_price * 100) / 100.0
        # check if market hours are over.
        if market_time >= self.end_time:
            self.end_of_day = True

        # check if last_minute has been defined
        if not self.last_minute:
            self.last_minute = minutes

        if market_price > self.high:
            self.high = market_price
            self.update_high_text(market_price)
            self.remake_graph()
        elif market_price < self.low:
            self.low = market_price
            self.update_low_text(market_price)
            self.remake_graph()
        # check if it has been a minute since the last update
        elif minutes != self.last_minute:
            # add a new line if so
            self.append_new_line(market_price)
            # update minute
            self.last_minute = minutes

        self.update_price_text(market_price, self.stock_len)
        if self.investment and market_price:
            # update the price and comparison text
            difference = market_price - self.investment
            difference = math.floor(difference * 100) / 100.0
            self.update_comparison_text(difference)

        # print(f"{self.stock_name}: EPOCH: {math.floor(market_time / 60)},"
        #      f" ${market_price}")

    def remake_graph(self):
        # update the graph data
        self.crumb, self.cookie = get_crumb()
        self.cleanup_graph()
        self.scrape_stock_data(get_limits=False)
        self.generate_graph()

    def append_new_line(self, price):
        self.line_seg.set_color(*SG.RED)
        # add the new value to the graph
        x_point = self.x
        # get the amount between high and low
        max_difference = self.high - self.low
        current_difference = self.high - price
        # divide to get the ratio between 0 and 1 for the graph
        # the point on the graph lies
        self.ratio = current_difference / max_difference
        # make the value lie between 0.5 and 1
        z_point = (self.ratio / 2.0) + 0.5
        # apply multiplier
        z_point *= SG.Z_MULTIPLIER
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

    def cleanup_graph(self):
        for line in self.graph_nodes:
            line.remove_node()
        self.draw_sequence.finish()
        self.draw_sequence = Sequence()
        if self.line_seg:
            self.line_seg.reset()
            self.line_seg = None
