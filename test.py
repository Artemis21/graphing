from graphing import *
from PIL import ImageFont


BACKGROUND = (44, 47, 51, 255)
PLOT_COLOUR = (114, 137, 218, 255)
PLOT_2_COLOUR = (210, 31, 60, 255)
TEXT_COLOUR = (255, 255, 255, 255)
FONT = ImageFont.truetype('../fonts/Roboto/Roboto-Bold.ttf', size=20)

DATA = {0: 3, 1: 5, 2: 3, 3: 0, 4: 3, 5: 3}
X_LABELS = ['a', 'b', 'c', 'd', 'e', 'f']


x_axis = Axis.text(
    X_LABELS, 'x', colour=TEXT_COLOUR, gap=100, font=FONT, rotation=45
)
y_axis = Axis.range(6, 'y', colour=TEXT_COLOUR, gap=100, font=FONT, label='Value')
plot_1 = BarPlot(
    list(DATA.values())[:-1], bar_padding=10, bar_width=80,
    colour=PLOT_2_COLOUR, scale=100
)
plot_2 = LinePlot(
    DATA, x_scale=100, y_scale=100, line_width=5, dot_size=5,
    line_colour=PLOT_COLOUR, dot_colour=PLOT_COLOUR
)
graph = Graph(x_axis, y_axis, [plot_1, plot_2], background=BACKGROUND)

graph.save('test.png')
