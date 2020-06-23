![CC-BY-NC-SA-4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)

---
# Graphing

> This library is not maintained - WYSIWYG.
> The docs are below, refer to test.py for an example (even by my standards though, that file is badly formatted).
> Alternatives include matplotlib and plotnine, though I created this because I had issues with those.

This library creates PIL images of graphs. It currently only supports line graphs and bar graphs.

## Concept

A graph is made out of components. Currently, those are:
 - An X axis
 - A Y axis
 - An arbitrary number of plots

## Graph

The `Graph` class is the main image. Example:
```python
graph = Graph(x_axis, y_axis, [plot_1, plot_2])
graph.save('graph.png')
```
It also has the following optional arguments:
 - `legend`: currently unsuported, so must be `None` (defualt).
 - `padding`: padding around the graph, in pixels. Defaults to `20`.
 - `background`: a four tuple representing the background colour. Defaults to `(0, 0, 0, 0)` (fully transparent).

It has the following methods:
 - `def show()`: display the image on the screen (primarily for debugging)
 - `def save(file, format=None)`: save the image to a file path or file like object. Format is inferred from the file name if not given.

## Axes

The `Axis` class represents an axis. It has the following arguments:
 - `ticks`: a dict of `{position: label}`, where `position` is the tick position in pixels, and `label` is the tick's label.
 - `orientation`: either `x` or `y`.
 - `label`: a label for the axis, eg. `Distance/m`. Defaults to the empty string.
 - `rotation`: the number of degrees clockwise to rotate the tick labels. Defaults to `270` for the horizontal axis or `0` for the vertical axis.
 - `colour`: the colour for the ticks, tick labels and line. Defaults to `(0, 0, 0, 255)` (black).
 - `font`: the font to use for tick labels. Defaults to PIL's "better than nothing" default font.
 - `label_font`: the font to use for the label. Defaults to `font`.
 - `label_colour`: the colour to use for the label. Defaults to `colour`.
 - `label_padding`: the distance in pixels between the label and the tick labels. Defaults to `10`.
 - `tick_padding`: the distance in pixels between the tick labels and the ticks. Defaults to `2`.
 - `tick_length`: the length of the tick in pixels. Defaults to `4`.

For convenience, `Axis` also has the following constructors:
 - `def numerical(ticks, *, scale=20)`: create an `Axis` with numerical ticks, where `ticks` is a list of numbers, and `scale` is the number of pixels per integer.
 - `def range(end, *, start=0, step=1, gap=20)`: create an `Axis` with evenly distributed numbers in the range `[start, stop)`, with step `step`, and `gap` pixels per integer.
 - `def text(labels, *, gap=20)`: create an `Axis` with evenly distributed textual labels, and `gap` pixels between each label.

All of these constructors also accept the arguments given to `Axis.__init__`.

## Plots

All plots inherit from `Plot`. The following plots are defined:

### LinePlot

This represents a line graph. It accepts the following arguments:
 - `points`: a dict of `{x: y}` pixel coordinates for the plot.
 - `padding_left`: the number of pixels to leave blank on the left of the plot. Defaults to `0`.
 - `padding_right`: the number of pixels to leave blank on the right of the plot. Defaults to `20`.
 - `padding_top`: the number of pixels to leave blank above the plot. Defaults to `20`.
 - `padding_bottom`: the number of pixels to leave blank below the plot. Defaults to `0`.
 - `x_scale`: the number of pixels per integer horizontally. Defaults to `20`.
 - `y_scale`: the number of pixels per integer vertically. Defaults to `20`.
 - `dot_size`: the size, in pixels, of the dot at each point. Defaults to `2`.
 - `dot_colour`: the colour of the dot at each point. Defaults to `(0, 0, 255, 255)` (blue).
 - `line_width`: the width of the line. Defaults to `2`.
 - `line_colour`: the colour of the line. Defaults to`(0, 0, 255, 255)` (blue).

### BarPlot

This represents a bar graph. It accepts the following arguments:
 - `values`: a list of values for the bars, in order.
 - `bar_padding`: the distance in pixels on either side of each bar (half the distance between bars). Defaults to `5`.
 - `bar_width`: the width in pixels of each bar. Defaults to `10`.
 - `padding_top`: the number of pixels to leave blank above the plot. Defaults to `20`.
 - `colour`: the colour of the bars. Defaults to`(0, 0, 255, 255)` (blue).
 - `scale`: the number of pixels per integer vertically. Defaults to `20`.
