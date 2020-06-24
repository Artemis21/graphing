"""The main plot on a graph."""
import math

from PIL import Image, ImageDraw


class Plot:
    """Base class for a plot."""

    def __init__(self, image: Image):
        self.img = image
        self.width, self.height = image.size


class LinePlot(Plot):
    """Class for line graphs."""

    def __init__(
            self, points, padding_left=0, padding_right=20, padding_top=20,
            padding_bottom=0, x_scale=20, y_scale=20, dot_size=2,
            dot_colour=(0, 0, 255, 255), line_width=2,
            line_colour=(0, 0, 255, 255)):
        """Create a line graph."""
        x_offset = padding_left - min(points) * x_scale
        y_offset = padding_bottom - min(points.values()) * y_scale
        self.width = math.ceil(
            (max(points) - min(points)) * x_scale
            + padding_right + padding_left
        )
        self.height = math.ceil(
            (max(points.values()) - min(points.values())) * y_scale
             + padding_top + padding_bottom
        )
        image = Image.new(
            'RGBA', (self.width + 1, self.height + 1), color=(0, 0, 0, 0)
        )
        draw = ImageDraw.Draw(image)
        line = []
        for x_pos in sorted(points):
            x = x_offset + x_pos * x_scale
            y = self.height - y_offset - points[x_pos] * y_scale
            line.append((x, y))
            offset = dot_size // 2
            draw.ellipse(
                (x - offset, y - offset, x + offset, y + offset),
                fill=dot_colour
            )
        if line_width:
            draw.line(line, fill=line_colour, width=line_width)
        super().__init__(image)


class BarPlot(Plot):
    """Class for simple, fixed-with bar graphs."""

    def __init__(
            self, values, bar_padding=5, bar_width=10, padding_top=20,
            colour=(0, 0, 255, 255), scale=20
            ):
        """Create a bar graph."""
        self.width = math.ceil((bar_padding * 2 + bar_width) * len(values))
        self.height = math.ceil(scale * max(values) + padding_top)
        image = Image.new(
            'RGBA', (self.width + 1, self.height + 1), color=(0, 0, 0, 0)
        )
        draw = ImageDraw.Draw(image)
        for n, value in enumerate(values):
            x0 = n * (bar_padding * 2 + bar_width) + bar_padding
            x1 = x0 + bar_width
            y1 = self.height
            y0 = y1 - value * scale
            draw.rectangle((x0, y0, x1 + 1, y1 + 1), colour)
        super().__init__(image)
