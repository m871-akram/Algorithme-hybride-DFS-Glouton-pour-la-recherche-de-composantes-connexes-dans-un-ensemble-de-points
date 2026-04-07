"""
N-dimensional point with Euclidean geometry helpers.
"""

from __future__ import annotations

from math import sqrt
from typing import List

from geo.quadrant import Quadrant


class Point:
    """An N-dimensional point represented as a vector of floating-point coordinates.

    Examples:
        Create a 2D point and compute the distance to another::

            p1 = Point([2.0, 5.0])
            p2 = Point([5.0, 9.0])
            print(p1.distance_to(p2))  # 5.0
    """

    def __init__(self, coordinates: List[float]) -> None:
        """Initialise the point from a coordinate list.

        Args:
            coordinates: Ordered list of floating-point coordinates, one per
                dimension (e.g. ``[x, y]`` for 2D).
        """
        self.coordinates = coordinates

    def copy(self) -> "Point":
        """Return a deep copy of this point.

        Returns:
            A new :class:`Point` with the same coordinates.
        """
        return Point(list(self.coordinates))

    def distance_to(self, other: "Point") -> float:
        """Compute the Euclidean distance to *other*.

        The method is symmetric: ``p1.distance_to(p2) == p2.distance_to(p1)``.

        Args:
            other: The target point.

        Returns:
            Non-negative Euclidean distance between the two points.
        """
        if self < other:
            # Delegate to the other point so that the expensive branch is only
            # computed once regardless of call order.
            return other.distance_to(self)

        total = 0.0
        for c1, c2 in zip(self.coordinates, other.coordinates):
            diff = c1 - c2
            total += diff * diff

        return sqrt(total)

    def bounding_quadrant(self) -> Quadrant:
        """Return the tightest axis-aligned bounding box containing this point.

        Required by the ``tycat`` display system.

        Returns:
            A degenerate :class:`~geo.quadrant.Quadrant` whose min and max
            coordinates both equal this point's coordinates.
        """
        return Quadrant(self.coordinates, self.coordinates)

    def svg_content(self) -> str:
        """Return an SVG ``<use>`` element placing the point symbol.

        Returns:
            SVG markup string consumed by :func:`~geo.tycat.tycat`.
        """
        return '<use xlink:href="#c" x="{}" y="{}"/>\n'.format(*self.coordinates)

    def cross_product(self, other: "Point") -> float:
        """Compute the 2D cross product of two vectors anchored at the origin.

        Args:
            other: The second 2D vector.

        Returns:
            Scalar value ``x1*y2 - y1*x2``.
        """
        x1, y1 = self.coordinates
        x2, y2 = other.coordinates
        return x1 * y2 - y1 * x2

    # ------------------------------------------------------------------
    # Arithmetic operators (enable vector algebra on points)
    # ------------------------------------------------------------------

    def __add__(self, other: "Point") -> "Point":
        """Component-wise addition (useful for translations).

        Args:
            other: Point whose coordinates are added to this one.

        Returns:
            New :class:`Point` representing the sum.
        """
        return Point([i + j for i, j in zip(self.coordinates, other.coordinates)])

    def __sub__(self, other: "Point") -> "Point":
        """Component-wise subtraction (useful for computing displacement vectors).

        Args:
            other: Point to subtract from this one.

        Returns:
            New :class:`Point` representing the difference.
        """
        return Point([i - j for i, j in zip(self.coordinates, other.coordinates)])

    def __mul__(self, factor: float) -> "Point":
        """Scalar multiplication (useful for scaling).

        Args:
            factor: Scalar multiplier.

        Returns:
            New :class:`Point` with each coordinate scaled by *factor*.
        """
        return Point([c * factor for c in self.coordinates])

    def __truediv__(self, factor: float) -> "Point":
        """Scalar division (useful for normalisation).

        Args:
            factor: Non-zero divisor.

        Returns:
            New :class:`Point` with each coordinate divided by *factor*.
        """
        return Point([c / factor for c in self.coordinates])

    def __str__(self) -> str:
        return ", ".join(str(c) for c in self.coordinates)

    def __repr__(self) -> str:
        return "Point([" + ", ".join(str(c) for c in self.coordinates) + "])"

    def __lt__(self, other: "Point") -> bool:
        """Lexicographical ordering used to guarantee a canonical call direction
        in :meth:`distance_to`.

        Args:
            other: Point to compare against.

        Returns:
            ``True`` if this point is lexicographically smaller than *other*.
        """
        return self.coordinates < other.coordinates
