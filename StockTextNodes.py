import math

from panda3d.core import TextNode

import StockGlobals as SG


class StockTextNodes:

    def __init__(self, stock_name, node):
        self.stock_name = stock_name
        self.node = node
        self.stock_text = None
        self.stock_text_node = None
        self.comparison_text = None
        self.investment_text = None
        self.price_text = None
        self.price_text_node = None
        self.last_price = None
        self.investment = None

    def generate_company_text(self):
        self.stock_text = TextNode("stock_text")
        self.stock_text.set_text(self.stock_name)
        self.stock_text.set_shadow(0.05, 0.05)
        self.stock_text_node = self.node.attach_new_node(self.stock_text)
        self.stock_text_node.set_pos(SG.STOCK_POS)
        self.stock_text_node.set_scale(SG.STOCK_SCALE)
        self.stock_text_node.set_depth_write(0)

    def generate_price_text(self, price):
        decimal_price = math.floor(price * 100) / 100.0
        string_price = str(decimal_price)
        self.price_text = TextNode("price_text")
        self.price_text.set_text(string_price)
        self.price_text.set_shadow(0.05, 0.05)
        self.price_text_node = self.node.attach_new_node(self.price_text)
        self.price_text_node.set_pos(SG.TEXT_POS)
        self.price_text_node.set_scale(SG.TEXT_SCALE)
        self.price_text_node.set_depth_write(0)

    def generate_investment_comparison(self, investment, current_price):
        self.investment = investment
        self.investment_text = TextNode('investment')
        self.investment_text.set_text(str(investment))
        self.investment_text.set_shadow(0.05, 0.05)
        self.investment_text.set_align(TextNode.ACenter)
        self.investment_text_node = self.node.attach_new_node(
                                                        self.investment_text)
        self.investment_text_node.set_pos(SG.INVEST_POS)
        self.investment_text_node.set_scale(SG.INVEST_SCALE)
        self.investment_text_node.set_depth_write(0)
        self.investment_text_node.set_color_scale(*SG.GOLD)

        self.comparison_text = TextNode('compare_price')
        difference = current_price - investment
        difference = math.floor(difference * 100)/100.0
        self.comparison_text.set_text(str(difference))
        self.comparison_text.set_shadow(0.05, 0.05)
        self.comparison_text.set_align(TextNode.ACenter)
        self.comparison_text_node = self.node.attach_new_node(
                                                        self.comparison_text)
        self.comparison_text_node.set_pos(SG.COMPARE_POS)
        self.comparison_text_node.set_scale(SG.COMPARE_SCALE)
        self.comparison_text_node.set_depth_write(0)

        self.color_investment(difference)

    def color_investment(self, difference):
        if difference > 0:  #  gain
            self.comparison_text_node.set_color_scale(*SG.GREEN)
        elif difference < 0:  #  loss
            self.comparison_text_node.set_color_scale(*SG.RED)
        else:
            self.comparison_text_node.set_color_scale(*SG.GRAY)

    def update_comparison_text(self, difference):
        self.comparison_text.set_text(str(difference))
        self.color_investment(difference)

    def update_price_text(self, price):
        if price > self.last_price:  # price increase
            color = SG.GREEN
        elif price < self.last_price:  # price decrease
            color = SG.RED
        else:
            color = SG.GRAY  # no change

        string_price = str(math.floor(price * 100) / 100.0)
        self.price_text.set_text(string_price)
        self.price_text_node.colorScaleInterval(4.5, (1, 1, 1, 1), color,
                                                blendType='easeIn').start()
        self.last_price = price
