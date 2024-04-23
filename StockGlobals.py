FINANCE_URL = "https://query1.finance.yahoo.com/"
CRUMB = "v1/test/getcrumb"
COMPANY_DATA = "v10/finance/quoteSummary/"
CHART_DATA = "v8/finance/chart/"

YAHOO_FINANCE_WEBSITE = "https://fc.yahoo.com"
USER_AGENT = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
              '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
TRADE_PERIOD = "currentTradingPeriod"

CHART_INTERVAL = ["1m", "2m", "5m"]
CHART_RANGE = ["1d", "5d", "1m", "6m", "ytd", "1y", "5y"]

WIN_SIZE = "1600, 600"
MARKET_DURATION = 390  # this is in minutes
PAUSE_DURATION = 1.0  # time between web scrapes.

LINE_THICKNESS = 2.0
Z_RATIO = 175
X_MULTIPLIER = 6
GRAPH_SCALE = 0.4

# TextNode
STOCK_POS = (-10, -.5, -10)
STOCK_SCALE = 2.0
TEXT_POS = (10, -.5, -10)
TEXT_SCALE = 2.0

X_POS = 15
Z_POS = 10
GRAPH_POSITIONS = [
    (-X_POS, 0, Z_POS / 2),
    (0, 0, Z_POS / 2),
    (X_POS, 0, Z_POS / 2),
    (-X_POS, 0, -Z_POS / 2 + 2),
    (0, 0, -Z_POS / 2 + 2),
    (-X_POS, 0, -Z_POS / 2 + 2),
]
