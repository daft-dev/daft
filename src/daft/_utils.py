"""Daft utilities."""

__all__: list[str] = []

import matplotlib.pyplot as plt
import numpy as np


class _rendering_context:
    """
    :param shape:
        The number of rows and columns in the grid.

    :param origin:
        The coordinates of the bottom left corner of the plot.

    :param grid_unit:
        The size of the grid spacing measured in centimeters.

    :param node_unit:
        The base unit for the node size. This is a number in centimeters that
        sets the default diameter of the nodes.

    :param observed_style:
        How should the "observed" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param alternate_style: (optional)
        How should the "alternate" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param node_ec:
        The default edge color for the nodes.

    :param node_fc:
        The default face color for the nodes.

    :param plate_fc:
        The default face color for plates.

    :param directed:
        Should the edges be directed by default?

    :param aspect:
        The default aspect ratio for the nodes.

    :param label_params:
        Default node label parameters.

    :param dpi: (optional)
        The DPI value to use for rendering.

    """

    def __init__(self, **kwargs):
        # Save the style defaults.
        self.line_width = kwargs.get("line_width", 1.0)

        # Make sure that the observed node style is one that we recognize.
        self.observed_style = kwargs.get("observed_style", "shaded").lower()
        styles = ("shaded", "inner", "outer")
        if self.observed_style not in styles:
            raise ValueError(
                f"Unrecognized observed node style: {self.observed_style}\n"
                f"\tOptions are: {', '.join(styles)}"
            )

        # Make sure that the alternate node style is one that we recognize.
        self.alternate_style = kwargs.get("alternate_style", "inner").lower()
        if self.alternate_style not in styles:
            raise ValueError(
                f"Unrecognized observed node style: {self.alternate_style}\n"
                f"\tOptions are: {', '.join(styles)}"
            )

        # Set up the figure and grid dimensions.
        self.padding = 0.1
        self.shp_fig_scale = 2.54

        self.shape = np.array(kwargs.get("shape", [1, 1]), dtype=np.float64)
        self.origin = np.array(kwargs.get("origin", [0, 0]), dtype=np.float64)
        self.grid_unit = kwargs.get("grid_unit", 2.0)
        self.figsize = self.grid_unit * self.shape / self.shp_fig_scale

        self.node_unit = kwargs.get("node_unit", 1.0)
        self.node_ec = kwargs.get("node_ec", "k")
        self.node_fc = kwargs.get("node_fc", "w")
        self.plate_fc = kwargs.get("plate_fc", "w")
        self.directed = kwargs.get("directed", True)
        self.aspect = kwargs.get("aspect", 1.0)
        self.label_params = dict(kwargs.get("label_params", {}) or {})

        self.dpi = kwargs.get("dpi", None)

        # Initialize the figure to ``None`` to handle caching later.
        self._figure = None
        self._ax = None

    def reset_shape(self, shape, adj_origin=False):
        """Reset the shape and figure size."""
        # shape is scaled by grid_unit
        # so divide by grid_unit for proper shape
        self.shape = shape / self.grid_unit + self.padding
        self.figsize = self.grid_unit * self.shape / self.shp_fig_scale

    def reset_origin(self, origin, adj_shape=False):
        """Reset the origin."""
        # origin is scaled by grid_unit
        # so divide by grid_unit for proper shape
        self.origin = origin / self.grid_unit - self.padding
        if adj_shape:
            self.shape -= self.origin
            self.figsize = self.grid_unit * self.shape / self.shp_fig_scale

    def reset_figure(self):
        """Reset the figure."""
        self.close()

    def close(self):
        """Close the figure if it is set up."""
        if self._figure is not None:
            plt.close(self._figure)
            self._figure = None
            self._ax = None

    def figure(self):
        """Return the current figure else create a new one."""
        if self._figure is not None:
            return self._figure
        args = {"figsize": self.figsize}
        if self.dpi is not None:
            args["dpi"] = self.dpi
        self._figure = plt.figure(**args)
        return self._figure

    def ax(self):
        """Return the current axes else create a new one."""
        if self._ax is not None:
            return self._ax

        # Add a new axis object if it doesn't exist.
        self._ax = self.figure().add_axes(
            (0, 0, 1, 1), frameon=False, xticks=[], yticks=[]
        )

        # Set the bounds.
        l0 = self.convert(*self.origin)
        l1 = self.convert(*(self.origin + self.shape))
        self._ax.set_xlim(l0[0], l1[0])
        self._ax.set_ylim(l0[1], l1[1])

        return self._ax

    def convert(self, *xy):
        """
        Convert from model coordinates to plot coordinates.

        """
        if len(xy) != 2:
            raise ValueError(
                "You must provide two coordinates to `convert()`."
            )
        return self.grid_unit * (np.atleast_1d(xy) - self.origin)


def _pop_multiple(_dict, default, *args):
    """
    A helper function for dealing with the way that matplotlib annoyingly
    allows multiple keyword arguments. For example, ``edgecolor`` and ``ec``
    are generally equivalent but no exception is thrown if they are both
    used.

    *Note: This function does throw a :class:`TypeError` if more than one
    of the equivalent arguments are provided.*

    :param _dict:
        A :class:`dict`-like object to "pop" from.

    :param default:
        The default value to return if none of the arguments are provided.

    :param *args:
        The arguments to try to retrieve.

    """
    if len(args) == 0:
        raise ValueError("You must provide at least one argument to `pop()`.")

    results = []
    for arg in args:
        try:
            results.append((arg, _dict.pop(arg)))
        except KeyError:
            pass

    if len(results) > 1:
        raise TypeError(
            "The arguments ({}) are equivalent, you can only provide one of them.".format(
                ", ".join([key for key, value in results])
            )
        )

    if len(results) == 0:
        return default

    return results[0][1]
