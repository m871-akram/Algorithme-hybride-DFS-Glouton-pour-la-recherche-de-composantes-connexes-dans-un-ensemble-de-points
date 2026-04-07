"""
Axis-aligned bounding boxes (quadrants) for geometric objects.

Quadrants are used by the ``tycat`` display system to compute image dimensions
and stroke sizes.
"""

from __future__ import annotations

from typing import List, Tuple


class Quadrant:
    """An axis-aligned rectangular bounding box in N-dimensional space.

    A quadrant is fully described by two coordinate arrays: ``min_coordinates``
    (the lower-left corner) and ``max_coordinates`` (the upper-right corner).

    Examples:
        Create a quadrant enclosing the unit square::

            q = Quadrant([0.0, 0.0], [1.0, 1.0])
    """

    def __init__(
        self, min_coordinates: List[float], max_coordinates: List[float]
    ) -> None:
        """Initialise a quadrant from explicit min/max coordinate arrays.

        Args:
            min_coordinates: Lower bounds for each dimension.
            max_coordinates: Upper bounds for each dimension.
        """
        self.min_coordinates = list(min_coordinates)
        self.max_coordinates = list(max_coordinates)

    def copy(self) -> "Quadrant":
        """Return a deep copy of this quadrant.

        Returns:
            New :class:`Quadrant` with independent coordinate lists.
        """
        return Quadrant(list(self.min_coordinates), list(self.max_coordinates))

    @classmethod
    def empty_quadrant(cls, dimension: int) -> "Quadrant":
        """Create an infinitely empty quadrant in *dimension*-D space.

        The min coordinates are set to ``+inf`` and the max coordinates to
        ``-inf`` so that any subsequent :meth:`add_point` or :meth:`update`
        call will tighten the bounds correctly.

        Args:
            dimension: Number of spatial dimensions.

        Returns:
            An empty (inverted-infinity) :class:`Quadrant`.
        """
        min_coords = [float("+inf")] * dimension
        max_coords = [float("-inf")] * dimension
        return cls(min_coords, max_coords)

    def add_point(self, added_point: "Point") -> None:  # type: ignore[name-defined]
        """Expand this quadrant so that it contains *added_point*.

        Args:
            added_point: A :class:`~geo.point.Point` whose coordinates are
                used to update the bounding box.
        """
        for i, coord in enumerate(added_point.coordinates):
            if coord < self.min_coordinates[i]:
                self.min_coordinates[i] = coord
            if coord > self.max_coordinates[i]:
                self.max_coordinates[i] = coord

    def update(self, other: "Quadrant") -> None:
        """Expand this quadrant to also contain *other*.

        After this call, ``self`` is the smallest quadrant that encloses both
        the original ``self`` and *other*.

        Args:
            other: Another :class:`Quadrant` in the same dimensional space.

        Raises:
            AssertionError: If *other* has a different number of dimensions.
        """
        assert len(self.min_coordinates) == len(other.min_coordinates), (
            "Cannot merge quadrants from different dimensional spaces."
        )
        for i, coord in enumerate(other.min_coordinates):
            if self.min_coordinates[i] > coord:
                self.min_coordinates[i] = coord
        for i, coord in enumerate(other.max_coordinates):
            if self.max_coordinates[i] < coord:
                self.max_coordinates[i] = coord

    def limits(self, index: int) -> Tuple[float, float]:
        """Return the min and max bounds for one coordinate axis.

        Args:
            index: Zero-based coordinate index (e.g. ``0`` for X, ``1`` for Y).

        Returns:
            ``(min_value, max_value)`` for the requested axis.
        """
        return (self.min_coordinates[index], self.max_coordinates[index])

    def inflate(self, distance: float) -> None:
        """Expand this quadrant outward by *distance* on every side.

        After inflation the quadrant contains all points that were within
        *distance* of the original boundary — useful for building spatial
        neighbourhood queries.

        Args:
            distance: Non-negative expansion amount.
        """
        self.min_coordinates = [c - distance for c in self.min_coordinates]
        self.max_coordinates = [c + distance for c in self.max_coordinates]

    def get_arrays(self) -> Tuple[List[float], List[float]]:
        """Return the raw min and max coordinate arrays.

        Returns:
            A tuple ``(min_coordinates, max_coordinates)``.
        """
        return (self.min_coordinates, self.max_coordinates)
