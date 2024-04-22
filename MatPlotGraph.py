import matplotlib.pyplot as plot
import numpy as np

from StockViewer.StockScrapper import StockScrapper

import StockGlobals as SG


def draw_chart_graph(graph_points, high):
    x_points = []
    y_points = []
    i = 0
    for point in graph_points:
        if point:
            # determine x value based on market duration
            x_point = (i / SG.MARKET_DURATION) * (SG.MARKET_DURATION / 10)
            x_points.append(x_point)

            # determine y value based on max high and the ratio
            y_point = (point / high) * SG.Z_RATIO
            y_points.append(y_point)
        i += 1
    x_points = np.array(x_points)
    y_points = np.array(y_points)

    plot.plot(x_points, y_points)
    plot.show()

scrapper = StockScrapper()
draw_chart_graph(scrapper.graph_points, scrapper.high)
