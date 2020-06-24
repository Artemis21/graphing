"""Class for various axes."""
import typing
import math

from PIL import Image, ImageDraw, ImageFont


def deg_to_rad(degrees):
    """Convert degrees to radians."""
    return degrees * (math.pi / 180)


def calculate_rotated_size(width, height, rotation):
    """Calculate the bounding box of a rectangle once it has been rotated."""
    rotation = deg_to_rad(rotation)
    right = deg_to_rad(90)
    r_width = (
        abs(math.sin(rotation) * height)
        + abs(math.sin(right - rotation) * width)
    )
    r_height = abs(
        abs(math.sin(right - rotation) * height)
        + abs(math.sin(rotation) * width)
    )
    return math.ceil(abs(r_width)), math.ceil(abs(r_height))


def draw_rotated_text(image, position, angle, text, font, colour):
    """Draw rotated text onto an image."""
    size = font.getsize(text)
    text_layer = Image.new('RGBA', size)
    draw = ImageDraw.Draw(text_layer)
    draw.text((0, 0), text, colour, font)
    rotated = text_layer.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
    image.paste(rotated, position, rotated)


class Axis:
    """Base class for axes."""

    @classmethod
    def numerical(cls, ticks, *args, scale=20, **kwargs):
        """Constructor for numerical axis."""
        ticks = {round(pos * scale): str(pos) for pos in ticks}
        return cls(ticks, *args, **kwargs)

    @classmethod
    def range(cls, end, *args, start=0, step=1, gap=20, **kwargs):
        """Constructor for a linear range axis."""
        return cls.numerical(
            range(start, end, step), *args, scale=gap // step, **kwargs
        )

    @classmethod
    def text(cls, labels, *args, gap=20, center=False, **kwargs):
        """Constructor for evenly placed textual labels."""
        ticks = {}
        pos = gap // 2 if center else 0
        for label in labels:
            ticks[pos] = label
            pos += gap
        if center:
            ticks[pos - gap // 2] = ''
        return cls(ticks, *args, **kwargs)

    def __init__(
            self, ticks, orientation, label='', rotation=None,
            colour=(0, 0, 0, 255), font=ImageFont.load_default(),
            label_font=None, label_colour=None, label_padding=10,
            tick_padding=2, tick_length=5):
        self.ticks = ticks
        self.orientation = orientation.lower()
        self.label = label
        if rotation is None:
            self.rotation = 90 if orientation == 'x' else 0
        else:
            self.rotation = 360 - rotation
        self.colour = colour
        self.font = font
        self.label_font = label_font or font
        self.label_colour = label_colour or colour
        self.label_padding = label_padding if label else 0
        self.tick_padding = tick_padding
        self.tick_length = tick_length
        self.calculate_size()
        self.draw_line()
        self.draw_ticks()
        self.draw_label()

    def calculate_size(self):
        """Calculate the sizes of everything."""
        label_width, label_height = self.label_font.getsize(self.label)
        self.label_width = label_width + self.label_padding
        self.label_height = label_height + self.label_padding
        self.tick_width = max(
            calculate_rotated_size(
                *self.font.getsize(self.ticks[position]), self.rotation
            )[1]
            for position in self.ticks
        )
        length = math.ceil(max(self.ticks))
        depth = math.ceil(
            self.tick_padding
            + self.tick_length
            + self.tick_width
            + self.label_height
        )
        if self.orientation == 'x':
            self.width = length
            self.height = depth
        else:
            self.width = depth
            self.height = length
        self.img = Image.new(
            'RGBA', (self.width + 1, self.height + 1), color=(0, 0, 0, 0)
        )
        self.draw = ImageDraw.Draw(self.img)

    def draw_line(self):
        """Draw the main line of the axis."""
        if self.orientation == 'x':
            self.draw.line(((0, 0), (self.width, 0)), self.colour)
        else:
            self.draw.line(
                ((self.width, 0), (self.width, self.height)),
                self.colour
            )

    def draw_label(self):
        """Draw the label."""
        if self.label:
            angle = 0 if self.orientation == 'x' else 90
            text_width, text_height = calculate_rotated_size(
                *self.label_font.getsize(self.label), angle
            )
            if self.orientation == 'x':
                draw_rotated_text(
                    self.img,
                    ((self.width - text_width) // 2, self.height - text_height),
                    angle, self.label, self.label_font,
                    self.label_colour
                )
            else:
                draw_rotated_text(
                    self.img,
                    (0, (self.height - text_height) // 2),
                    angle, self.label, self.label_font,
                    self.label_colour
                )

    def draw_ticks(self):
        """Draw the ticks on the line."""
        for position in self.ticks:
            text_width, text_height = calculate_rotated_size(
                *self.font.getsize(self.ticks[position]), self.rotation
            )
            if self.orientation == 'x':
                half_w = text_width // 2
                text_position = max(position - half_w, 0)
                text_position = min(text_position, self.width - text_width)
                draw_rotated_text(
                    self.img,
                    (text_position, self.tick_length + self.tick_padding),
                    self.rotation, self.ticks[position], self.font,
                    self.colour
                )
                self.draw.line(
                    ((position, 0), (position, self.tick_length)), self.colour
                )
            else:
                half_h = text_height // 2
                text_y = min(
                    max(self.height - position - half_h, 0),
                    self.height - text_height
                )
                text_x_position = (
                    self.width - self.tick_length - self.tick_padding
                    - text_width
                )
                draw_rotated_text(
                    self.img, (text_x_position, text_y), self.rotation,
                    self.ticks[position], self.font, self.colour
                )
                self.draw.line(
                    (
                        (self.width - self.tick_length, position),
                        (self.width, position)
                    ),
                    self.colour
                )
