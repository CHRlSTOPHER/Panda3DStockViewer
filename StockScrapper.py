import requests

import StockGlobals as SG


def get_crumb():
    request = requests.get(SG.YAHOO_FINANCE_WEBSITE)
    cookie_data = request.headers['set-cookie']
    cookie = cookie_data.split(";")[0]
    request = requests.get(SG.FINANCE_URL + SG.CRUMB,
                           headers={'user-agent': SG.USER_AGENT,
                                    'cookie': cookie})
    return request.text, cookie


class StockScrapper:

    def __init__(self):
        self.crumb = None
        self.cookie = None
        self.chart_data = None
        self.start_time = None
        self.end_time = None
        self.market_time = None
        self.market_price = None

        self.graph_points = None
        self.high = None
        self.company_data = None

        self.generate()

    def generate(self):
        # get the crumb and cookie
        self.crumb, self.cookie = get_crumb()
        # we define this to determine the past graph points
        self.chart_data = self.get_chart_data(SG.STOCK_NAME)
        result = self.chart_data["chart"]["result"][0]

        self.start_time = result["meta"][SG.TRADE_PERIOD]["regular"]["start"]
        self.end_time = result["meta"][SG.TRADE_PERIOD]["regular"]["end"]
        # get all the points of the graph that exist so far
        self.graph_points = result['indicators']['quote'][0]['close']
        self.high = self.get_high_price()

    def append_current_price(self):
        pass

    def e(self):
        self.company_data = self.get_company_data(SG.STOCK_NAME)
        result = self.company_data["quoteSummary"]["result"][0]
        self.market_time = result["price"]["regularMarketTime"]
        self.market_price = result["price"]["regularMarketPrice"]["raw"]

    def debug(self):
        print(self.company_data)
        print(f"Graph point length: {len(self.graph_points)}")
        print(f"Market price: {self.market_price}")
        print(f"High : {self.high}")
        print(f"Start time: {self.start_time}")
        print(f"Market time: {self.market_time}")
        print(f"End time: {self.end_time}")
        print(f"Market duration: {(self.end_time - self.start_time) / 60}")

    def get_chart_data(self, stock):
        chart_data = requests.get(f"{SG.FINANCE_URL}{SG.CHART_DATA}{stock}",
                                  params={"interval": "1m",
                                          "range": "1d",
                                          "includePrePost": "false"},
                                  headers={'user-agent': SG.USER_AGENT,
                                           'cookie': self.cookie})
        return chart_data.json()

    def get_company_data(self, stock, asset_profile=False):
        modules = "price"
        if asset_profile:
            modules = "price,assetProfile"
        company_data = requests.get(f"{SG.FINANCE_URL}{SG.COMPANY_DATA}"
                                    f"{stock}",
                                    params={'modules': modules,
                                            "crumb": self.crumb},
                                    headers={'user-agent': SG.USER_AGENT,
                                             'cookie': self.cookie})
        return company_data.json()

    def get_high_price(self):
        valid_points = []
        for point in self.graph_points:
            if point:
                valid_points.append(point)
        return max(*valid_points)
