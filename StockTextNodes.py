import math

from panda3d.core import TextNode

import StockGlobals as SG


class StockTextNodes:

    def __init__(self, stock_name, node):

        self.stock_name = stock_name
        self.node = node
        self.stock_text = None
        self.stock_text_node = None
        self.compare_text = None
        self.compare_text_node = None
        self.invest_text = None
        self.invest_text_node = None
        self.price_text = None
        self.price_text_node = None
        self.last_price = None
        self.high_text = None
        self.low_text = None
        self.last_close_text = None
        self.invest = None
        self.investment = None

    def generate_company_text(self):
        self.stock_text, self.stock_text_node = self.generate_text_node(
            "stock_text", self.stock_name)
        self.stock_text_node.set_pos(SG.STOCK_POS)
        self.stock_text_node.set_scale(SG.STOCK_SCALE)

    def generate_price_text(self, price):
        decimal_price = math.floor(price * 100) / 100.0
        string_price = str(decimal_price)
        self.price_text, self.price_text_node = self.generate_text_node(
            "price_text", string_price)
        self.price_text_node.set_pos(SG.TEXT_POS)
        self.price_text_node.set_scale(SG.TEXT_SCALE)

    def generate_investment_comparison(self, investment, current_price):
        self.invest = investment
        self.invest_text, self.invest_text_node = self.generate_text_node(
            "investment", str(investment), TextNode.ACenter)
        self.invest_text_node.set_pos(SG.INVEST_POS)
        self.invest_text_node.set_scale(SG.INVEST_SCALE)
        self.invest_text_node.set_color_scale(*SG.GOLD)

        difference = current_price - investment
        difference = math.floor(difference * 100) / 100.0
        self.compare_text, self.compare_text_node = self.generate_text_node(
            "compare_text", str(difference), TextNode.ACenter)
        self.compare_text_node.set_pos(SG.COMPARE_POS)
        self.compare_text_node.set_scale(SG.COMPARE_SCALE)

        self.color_investment(difference)

    def generate_limits_text(self, high, low, last_close):
        self.high_text, self.high_text_node = self.generate_text_node(
            "high_text", str(high), TextNode.ARight)
        self.low_text, self.low_text_node = self.generate_text_node(
            "low_text", str(low), TextNode.ARight)
        # last close text
        self.close_text, self.close_text_node = self.generate_text_node(
            "last_close_text", str(last_close), TextNode.ARight)
        self.high_text_node.set_pos(SG.HIGH_TEXT_POS)
        self.low_text_node.set_pos(SG.LOW_TEXT_POS)
        self.close_text_node.set_x(SG.CLOSE_TEXT_X)
        for text in [self.high_text_node, self.low_text_node,
                     self.close_text_node]:
            text.set_scale(SG.LIMIT_TEXT_SCALE)


    def color_investment(self, difference):
        if difference > 0:  #  gain
            self.compare_text_node.set_color_scale(*SG.GREEN)
        elif difference < 0:  #  loss
            self.compare_text_node.set_color_scale(*SG.RED)
        else:
            self.compare_text_node.set_color_scale(*SG.GRAY)

    def update_comparison_text(self, difference):
        self.compare_text.set_text(str(difference))
        self.color_investment(difference)

    def update_price_text(self, price, stock_len):
        if price > self.last_price:  # price increase
            color = SG.GREEN
        elif price < self.last_price:  # price decrease
            color = SG.RED
        else:
            color = SG.GRAY  # no change

        string_price = str(math.floor(price * 100) / 100.0)
        self.price_text.set_text(string_price)
        self.price_text_node.colorScaleInterval(stock_len - .5,
                                                (1, 1, 1, 1), color,
                                                blendType='easeIn').start()
        self.last_price = price

    def update_high_text(self, high):
        self.high_text.set_text(str(high))

    def update_low_text(self, low):
        self.low_text.set_text(str(low))

    def generate_text_node(self, name, text, alignment=None):
        _text = TextNode(name)
        _text.set_text(text)
        _text.set_shadow(0.05, 0.05)
        if alignment:
            _text.set_align(alignment)
        text_node = self.node.attach_new_node(_text)
        text_node.set_depth_write(0)
        return _text, text_node
