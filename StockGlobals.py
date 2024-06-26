STOCK_JSON = "stocks.json"

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

WIN_SIZE = "1700 950"
BG_COLOR = (.2, .2, .25, 1)
BG_LINE_COLOR = (.85, .85, 1, 1)
BG_LINE_POS = [
    (-10.2, 0, -6.6),
    (17.9, 0, -6.6),
    (-10.2, 0, 6.6),
    (17.9, 0, 6.6),
]

MARKET_DURATION = 390  # this is in minutes
PAUSE_DURATION = 1.0  # time between web scrapes.
STOCK_LIMIT = 16

GREEN = (.2, 1, .2, 1)
RED = (1, .2, .2, 1)
GOLD = (1, 1, .75, 1)
GRAY = (.8, .8, .8, 1)

LINE_THICKNESS = 2.0
Z_MULTIPLIER = 100
X_MULTIPLIER = 6

GRAPH_POS = (-10, 0, 18)
GRAPH_SCALE = 0.375
# actual graph scale
GRAPH_SX = .07
GRAPH_SZ = -.24

# TextNode
STOCK_POS = (-10, -.5, -10)
STOCK_SCALE = 2.5
TEXT_POS = (10, -.5, -10)
TEXT_SCALE = 3.0
INVEST_POS = (0.0, 0, -9.25)
INVEST_SCALE = 1.9
COMPARE_POS = (6.25, 0, -10.25)
COMPARE_SCALE = 1.9
HIGH_TEXT_POS = (-11, 0, 6)
LOW_TEXT_POS = (-11, 0, -7)
CLOSE_TEXT_X = 18
LIMIT_TEXT_SCALE = 2.5

X_POS = 18
Z_POS = 10.75
M_1 = 1.5
M_2 = 0.5
GRAPH_POSITIONS = [
    (-X_POS * M_1, 0, Z_POS * M_1),
    (-X_POS * M_2, 0, Z_POS * M_1),
    (X_POS * M_2, 0, Z_POS * M_1),
    (X_POS * M_1, 0, Z_POS * M_1),

    (-X_POS * M_1, 0, Z_POS * M_2),
    (-X_POS * M_2, 0, Z_POS * M_2),
    (X_POS * M_2, 0, Z_POS * M_2),
    (X_POS * M_1, 0, Z_POS * M_2),

    (-X_POS * M_1, 0, Z_POS * -M_2),
    (-X_POS * M_2, 0, Z_POS * -M_2),
    (X_POS * M_2, 0, Z_POS * -M_2),
    (X_POS * M_1, 0, Z_POS * -M_2),

    (-X_POS * M_1, 0, Z_POS * -M_1),
    (-X_POS * M_2, 0, Z_POS * -M_1),
    (X_POS * M_2, 0, Z_POS * -M_1),
    (X_POS * M_1, 0, Z_POS * -M_1)
]
