"""Draw the data."""
import typing

from PIL import Image

from .axes import Axis
from .annotations import Legend
from .plots import Plot


class Graph:
    """A graph visual."""

    def __init__(
            self, x_axis: Axis, y_axis: Axis, plots: typing.List[Plot],
            legend: Legend = None, padding=10, background=(0, 0, 0, 0)):
        """Draw a graph."""
        width = max(plot.width for plot in plots) + y_axis.width + padding * 2
        height = (
            max(plot.height for plot in plots) + x_axis.height + padding * 2
        )
        self.img = Image.new('RGBA', (width, height), color=background)
        for plot in plots:
            self.img.paste(
                plot.img,
                (
                    padding + y_axis.width,
                    height - padding - x_axis.height - plot.height
                ),
                plot.img
            )
        self.img.paste(x_axis.img, (
            padding + y_axis.width, height - padding - x_axis.height
        ), x_axis.img)
        self.img.paste(y_axis.img, (
            padding, height - padding - x_axis.height - y_axis.height
        ), y_axis.img)
        if legend:
            self.img.paste(
                legend.img, (width - padding - legend.width, height - padding)
            )

    def show(self):
        """Use PIL's show method.

        Unix: display, eog or xv.
        MacOS: native Preview application.
        Windows: native Preview application.
        """
        self.img.show()

    def save(self, file, format: typing.Optional[str] = None):
        """Use PIL's save method."""
        self.img.save(file, format)
