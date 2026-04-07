"""
SVG-based graphical display system.

Saves geometric objects as SVG files and opens them in the Terminology terminal
emulator.  Each argument passed to :func:`tycat` is rendered in a distinct
colour.  Objects must implement ``bounding_quadrant()`` and ``svg_content()``,
or be iterables of such objects.
"""

from __future__ import annotations

import os
import getpass
from itertools import cycle
from typing import Any, List, Tuple

from geo.quadrant import Quadrant


class Displayer:
    """Compute SVG layout parameters and write SVG files for a set of objects.

    Class attributes:
        svg_dimensions: Target SVG canvas size in pixels ``(width, height)``.
        svg_colors: Ordered list of colour names cycled across displayed objects.
        file_count: Monotonically increasing counter used to generate unique
            filenames in ``/tmp/<user>/``.
    """

    svg_dimensions: Tuple[int, int] = (800, 600)
    svg_colors: List[str] = (
        "red green blue purple orange saddlebrown mediumseagreen "
        "darkolivegreen lightskyblue dimgray mediumpurple midnightblue "
        "olive chartreuse darkorchid hotpink darkred peru "
        "goldenrod mediumslateblue orangered darkmagenta "
        "darkgoldenrod mediumslateblue firebrick palegreen "
        "royalblue tan tomato springgreen pink orchid "
        "saddlebrown moccasin mistyrose cornflowerblue "
        "darkgrey"
    ).split()
    file_count: int = 0

    def __init__(self, bounding_quadrant: Quadrant) -> None:
        """Compute the stroke size from the bounding quadrant.

        The stroke size is scaled so that lines remain visually consistent
        regardless of the coordinate range of the displayed objects.

        Args:
            bounding_quadrant: Axis-aligned bounding box enclosing all objects
                to be displayed.

        Raises:
            ValueError: If the bounding box is degenerate (zero width or height)
                or if the computed scale factor is zero.
        """
        min_coords, max_coords = bounding_quadrant.get_arrays()
        self.min_coordinates = min_coords
        self.max_coordinates = max_coords

        self.dimensions = [
            a - b for a, b in zip(self.max_coordinates, self.min_coordinates)
        ]

        if any(d == 0.0 for d in self.dimensions):
            raise ValueError("Bounding quadrant is flat (zero extent in one dimension).")

        ratios = [a / b for a, b in zip(self.svg_dimensions, self.dimensions)]
        scale = min(ratios)
        if scale == 0.0:
            raise ValueError("Computed SVG scale factor is zero.")

        # Stroke size in data coordinates: 3 pixels converted to the data space
        self.stroke_size = 3 / scale

    def open_svg(self, filename: str) -> Any:
        """Create and initialise a new SVG file.

        Writes the SVG header, background rectangle, and shared point-circle
        symbol definition.

        Args:
            filename: Absolute path where the SVG file will be written.

        Returns:
            The open file handle (must be closed via :meth:`close_svg`).
        """
        svg_file = open(filename, "w")
        svg_file.write('<svg width="{}" height="{}"'.format(*self.svg_dimensions))
        svg_file.write(' viewBox="{} {}'.format(*self.min_coordinates))
        svg_file.write(' {} {}"'.format(*self.dimensions))
        svg_file.write(' xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        svg_file.write('<rect x="{}" y="{}"'.format(*self.min_coordinates))
        svg_file.write(
            ' width="{}" height="{}" fill="white"/>\n'.format(*self.dimensions)
        )
        svg_file.write(
            '<defs><symbol id="c">'
            '<circle r="{}"/></symbol></defs>\n'.format(2 * self.stroke_size)
        )
        svg_file.write('<g stroke-width="{}" opacity="0.7">\n'.format(self.stroke_size))
        return svg_file

    def close_svg(self, svg_file: Any) -> None:
        """Finalise and close an open SVG file.

        Args:
            svg_file: File handle returned by :meth:`open_svg`.
        """
        svg_file.write("</g>\n")
        svg_file.write("</svg>\n")
        svg_file.close()


def tycat(*things: Any) -> None:
    """Graphically display one or more geometric objects in Terminology.

    Each positional argument is rendered in a different colour.  Objects must
    implement both ``bounding_quadrant()`` (returning a
    :class:`~geo.quadrant.Quadrant`) and ``svg_content()`` (returning an SVG
    string), or be iterables of such objects.

    Requires the `Terminology <https://www.enlightenment.org/about-terminology>`_
    terminal emulator to be the active terminal.

    Args:
        *things: Geometric objects or iterables of geometric objects to display.
    """
    print("[", Displayer.file_count, "]")

    # Store files in a per-user temp directory to avoid collisions
    user = getpass.getuser()
    directory = f"/tmp/{user}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = "{}/{}.svg".format(directory, str(Displayer.file_count).zfill(5))
    Displayer.file_count += 1

    size, svg_strings = compute_displays(things)
    try:
        display = Displayer(size)
    except ValueError:
        print(f"Displaying image {Displayer.file_count - 1} failed: bounding box is flat.")
        return

    svg_file = display.open_svg(filename)
    for string in svg_strings:
        svg_file.write(string)
    display.close_svg(svg_file)
    os.system(f"tycat {filename}")


def compute_displays(things: Any) -> Tuple[Quadrant, List[str]]:
    """Compute the combined bounding quadrant and SVG strings for all objects.

    Args:
        things: Iterable of objects or iterables of objects to display.

    Returns:
        A tuple ``(bounding_quadrant, svg_strings)`` ready to be passed to a
        :class:`Displayer`.
    """
    quadrant = Quadrant.empty_quadrant(2)
    strings: List[str] = []
    for color, thing in zip(cycle(iter(Displayer.svg_colors)), things):
        strings.append(f'<g fill="{color}" stroke="{color}">\n')
        inner_quadrant, inner_strings = compute_display(thing)
        quadrant.update(inner_quadrant)
        strings.extend(inner_strings)
        strings.append("</g>\n")

    return (quadrant, strings)


def compute_display(thing: Any) -> Tuple[Quadrant, List[str]]:
    """Compute the bounding quadrant and SVG content for a single object.

    Recursively handles iterables by processing each element and merging their
    bounding quadrants.

    Args:
        thing: A single geometric object (implementing ``bounding_quadrant`` and
            ``svg_content``) or an iterable of such objects.

    Returns:
        A tuple ``(bounding_quadrant, svg_strings)`` for *thing*.
    """
    quadrant = Quadrant.empty_quadrant(2)
    strings: List[str] = []
    try:
        iterator = iter(thing)
        for sub_thing in iterator:
            inner_quadrant, inner_strings = compute_display(sub_thing)
            strings.extend(inner_strings)
            quadrant.update(inner_quadrant)
    except TypeError:
        # thing is a leaf object — not iterable
        strings.append(thing.svg_content())
        quadrant.update(thing.bounding_quadrant())

    return quadrant, strings
