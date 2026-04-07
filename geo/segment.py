"""
Oriented line segment between two :class:`~geo.point.Point` objects.
"""

from __future__ import annotations

from typing import List

from geo.quadrant import Quadrant


class Segment:
    """An oriented segment defined by two endpoint :class:`~geo.point.Point` objects.

    Examples:
        Create a horizontal segment and measure its length::

            s = Segment([Point([1.0, 2.0]), Point([5.0, 2.0])])
            print(s.length())  # 4.0
    """

    def __init__(self, points: List["Point"]) -> None:  # type: ignore[name-defined]
        """Initialise the segment from a two-element point array.

        Args:
            points: List ``[start, end]`` of exactly two
                :class:`~geo.point.Point` objects.
        """
        self.endpoints = points

    def copy(self) -> "Segment":
        """Return a deep copy of this segment (endpoints are also copied).

        Returns:
            New :class:`Segment` with independent copies of both endpoints.
        """
        return Segment([p.copy() for p in self.endpoints])

    def length(self) -> float:
        """Compute the Euclidean length of this segment.

        Returns:
            Distance between the two endpoints.

        Example::

            Segment([Point([1, 1]), Point([5, 1])]).length()  # 4.0
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def bounding_quadrant(self) -> Quadrant:
        """Return the tightest axis-aligned bounding box enclosing this segment.

        Returns:
            A :class:`~geo.quadrant.Quadrant` that just contains both endpoints.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.endpoints:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self) -> str:
        """Return an SVG ``<line>`` element representing this segment.

        Returns:
            SVG markup string consumed by :func:`~geo.tycat.tycat`.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(
            *self.endpoints[0].coordinates, *self.endpoints[1].coordinates
        )

    def endpoint_not(self, point: "Point") -> "Point":  # type: ignore[name-defined]
        """Return the endpoint that is *not* equal to *point*.

        Args:
            point: One of the two endpoints.

        Returns:
            The other endpoint.
        """
        if self.endpoints[0] == point:
            return self.endpoints[1]
        return self.endpoints[0]

    def contains(self, possible_point: "Point") -> bool:  # type: ignore[name-defined]
        """Test whether *possible_point* lies on this segment.

        Uses the collinearity condition: a point P lies on segment AB if and
        only if ``dist(A, P) + dist(P, B) == dist(A, B)``.  A small epsilon
        tolerance is applied to handle floating-point rounding.

        Note:
            Points very close to an endpoint may yield incorrect results due to
            accumulated floating-point error.

        Args:
            possible_point: The candidate point.

        Returns:
            ``True`` if the point lies on this segment within tolerance.
        """
        total_dist = sum(possible_point.distance_to(p) for p in self.endpoints)
        return abs(total_dist - self.length()) < 1e-6

    def __str__(self) -> str:
        return (
            "Segment(["
            + str(self.endpoints[0])
            + ", "
            + str(self.endpoints[1])
            + "])"
        )

    def __repr__(self) -> str:
        return "[" + repr(self.endpoints[0]) + ", " + repr(self.endpoints[1]) + "])"

    def __hash__(self) -> int:
        return hash(tuple(self.endpoints))
