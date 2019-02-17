# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["PGM", "Node", "Edge", "Plate"]
__version__ = "0.0.4"

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import FancyArrow
from matplotlib.patches import Rectangle as Rectangle

import numpy as np


class PGM(object):
    """
    The base object for building a graphical model representation.

    :param shape:
        The number of rows and columns in the grid.

    :param origin:
        The coordinates of the bottom left corner of the plot.

    :param grid_unit: (optional)
        The size of the grid spacing measured in centimeters.

    :param node_unit: (optional)
        The base unit for the node size. This is a number in centimeters that
        sets the default diameter of the nodes.

    :param observed_style: (optional)
        How should the "observed" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param deterministic_style: (optional)
        How should the "deterministic" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param node_ec: (optional)
        The default edge color for the nodes.

    :param directed: (optional)
        Should the edges be directed by default?

    :param aspect: (optional)
        The default aspect ratio for the nodes.

    :param label_params: (optional)
        Default node label parameters.

    """
    def __init__(self, shape=None, origin=None,
                 grid_unit=2., node_unit=1.,
                 observed_style="shaded",
                 deterministic_style='inner',
                 line_width=1., node_ec="k",
                 directed=True, aspect=1.0,
                 label_params={}, dpi=None):
        self._nodes = {}
        self._edges = []
        self._plates = []
        self._dpi = dpi

        #if shape and origin are not given, pass a default
        # and we will determine at rendering time
        self.shape = shape
        self.origin = origin
        if shape is None:
            shape = [1, 1]
        if origin is None:
            origin = [0, 0]

        self._ctx = _rendering_context(shape=shape, origin=origin,
                                       grid_unit=grid_unit,
                                       node_unit=node_unit,
                                       observed_style=observed_style,
                                       deterministic_style=deterministic_style,
                                       line_width=line_width,
                                       node_ec=node_ec, directed=directed,
                                       aspect=aspect,
                                       label_params=label_params,
                                       dpi=dpi)

    def add_node(self, node, content='', x=0, y=0, scale=1., aspect=None,
                 observed=False, fixed=False, deterministic=False,
                 offset=[0., 0.], fontsize=None, plot_params={}, label_params=None,
                 shape="ellipse"):
        """
        Add a :class:`Node` to the model.

        :param node:
            The plain-text identifier for the nodeself.
            Can also be the :class:`Node` to retain backward compatibility.

        :param content:
            The display form of the variable.

        :param x:
            The x-coordinate of the node in *model units*.

        :param y:
            The y-coordinate of the node.

        :param scale: (optional)
            The diameter (or height) of the node measured in multiples of
            ``node_unit`` as defined by the :class:`PGM` object.

        :param aspect: (optional)
            The aspect ratio width/height for elliptical nodes; default 1.

        :param observed: (optional)
            Should this be a conditioned variable?

        :param fixed: (optional)
            Should this be a fixed (not permitted to vary) variable?
            If `True`, modifies or over-rides ``diameter``, ``offset``,
            ``facecolor``, and a few other ``plot_params`` settings.
            This setting conflicts with ``observed``.

    :param deterministic: (optional)
        Should this be a deterministic variable?

        :param offset: (optional)
            The ``(dx, dy)`` offset of the label (in points) from the default
            centered position.

        :param fontsize: (optional)
            The fontsize to use.

        :param plot_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.patches.Ellipse` constructor.

        :param label_param: (optional)
            Default value: None
            FIXME (undocumented)

        :param shape: (optional)
            String in {ellipse (default), rectangle}
            If rectangle, aspect and scale holds for rectangle

        """
        if isinstance(node, Node):
            _node = node
        else:
            _node = Node(node, content, x, y, scale, aspect,
                     observed, fixed, deterministic,
                     offset, fontsize, plot_params, label_params,
                     shape)

        self._nodes[_node.name] = _node

        return node

    def add_edge(self, name1, name2, directed=None,
                 xoffset=0, yoffset=0, plot_params={}, **kwargs):
        """
        Construct an :class:`Edge` between two named :class:`Node` objects.

        :param name1:
            The name identifying the first node.

        :param name2:
            The name identifying the second node. If the edge is directed,
            the arrow will point to this node.

        :param directed: (optional)
            Should this be a directed edge?

        :param plot_params: (optional)
            A dictionary of parameters to pass to the plotting command when
            rendering.

        """
        if directed is None:
            directed = self._ctx.directed

        e = Edge(self._nodes[name1], self._nodes[name2], directed=directed,
                 xoffset=xoffset, yoffset=yoffset, plot_params=plot_params)
        self._edges.append(e)

        return e

    def add_plate(self, plate, label=None, label_offset=[5, 5], shift=0,
                 position="bottom left", fontsize=None, rect_params=None, bbox=None):
        """
        Add a :class:`Plate` object to the model.

        :param plate:
            The rectangle describing the plate bounds in model coordinates.
            Can also be the :class:`Plate` to retain backward compatibility.

        :param label: (optional)
            A string to annotate the plate.

        :param label_offset: (optional)
            The x and y offsets of the label text measured in points.

        :param shift: (optional)
            The vertical "shift" of the plate measured in model units. This will
            move the bottom of the panel by ``shift`` units.

        :param position: (optional)
            One of ``"bottom left"`` or ``"bottom right"``.

        :param fontsize: (optional)
            The fontsize to use.

        :param rect_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.patches.Rectangle` constructor.

        """
        if isinstance(plate, Plate):
            _plate = plate
        else:
            _plate = Plate(plate, label, label_offset, shift,
                                 position, fontsize, rect_params, bbox)

        self._plates.append(_plate)

        return None

    def render(self, **kwargs):
        """
        Render the :class:`Plate`, :class:`Edge` and :class:`Node` objects in
        the model. This will create a new figure with the correct dimensions
        and plot the model in this area.

        """

        # self.dpi = kwargs.get('dpi', self._dpi)
        self._ctx.dpi = kwargs.get('dpi', self._dpi)

        # Auto-set shape
        # We pass through each object once to find the maximum coordinates
        if self.shape is None:
            def get_max(maxsize, artist):
                if isinstance(artist, Ellipse):
                    maxsize = np.maximum(maxsize, artist.center +
                                  np.array([artist.width, artist.height])/2)
                elif isinstance(artist, Rectangle):
                    maxsize = np.maximum(maxsize,
                                  np.array([artist._x0, artist._y0]) +
                                  np.array([artist._width, artist._height]))
                return maxsize

            maxsize = np.copy(self._ctx.origin)

            for plate in self._plates:
                artist = plate.render(self._ctx)
                maxsize = get_max(maxsize, artist)

            for name in self._nodes:
                if self._nodes[name].fixed:
                    self._nodes[name].offset[1] -= 12.5
                artist = self._nodes[name].render(self._ctx)
                maxsize = get_max(maxsize, artist)

            self._ctx.reset_shape(maxsize)

        # Pass through each object to find the minimum coordinates
        if self.origin is None:
            def get_min(minsize, artist):
                if isinstance(artist, Ellipse):
                    minsize = np.minimum(minsize, artist.center -
                        np.array([artist.width, artist.height])/2, dtype=np.float)
                elif isinstance(artist, Rectangle):
                    minsize = np.minimum(minsize,
                        np.array([artist._x0, artist._y0], dtype=np.float))
                return minsize

            minsize = np.copy(self._ctx.shape * self._ctx.grid_unit)

            for plate in self._plates:
                artist = plate.render(self._ctx)
                minsize = get_min(minsize, artist)

            for name in self._nodes:
                artist = self._nodes[name].render(self._ctx)
                minsize = get_min(minsize, artist)

            self._ctx.reset_origin(minsize, self.shape is None)

        # Clear the figure from rendering context
        self._ctx.reset_figure()

        # Render figure using
        self.figure = self._ctx.figure()
        self.ax = self._ctx.ax()

        for plate in self._plates:
            plate.render(self._ctx)

        for edge in self._edges:
            edge.render(self._ctx)

        for name in self._nodes:
            self._nodes[name].render(self._ctx)

        return self.ax

    def show(self, dpi=None, *args, **kwargs):
        self.render(dpi=dpi)
        plt.show(*args, **kwargs)

    def savefig(self, fname, *args, **kwargs):
        kwargs['bbox_inches'] = kwargs.get('bbox_inches', 'tight')
        kwargs['dpi'] = kwargs.get('dpi', self._dpi)
        self.figure.savefig(fname, *args, **kwargs)


class Node(object):
    """
    The representation of a random variable in a :class:`PGM`.

    :param name:
        The plain-text identifier for the node.

    :param content:
        The display form of the variable.

    :param x:
        The x-coordinate of the node in *model units*.

    :param y:
        The y-coordinate of the node.

    :param scale: (optional)
        The diameter (or height) of the node measured in multiples of
        ``node_unit`` as defined by the :class:`PGM` object.

    :param aspect: (optional)
        The aspect ratio width/height for elliptical nodes; default 1.

    :param observed: (optional)
        Should this be a conditioned variable?

    :param fixed: (optional)
        Should this be a fixed (not permitted to vary) variable?
        If `True`, modifies or over-rides ``diameter``, ``offset``,
        ``facecolor``, and a few other ``plot_params`` settings.
        This setting conflicts with ``observed``.

    :param deterministic: (optional)
        Should this be a deterministic variable?

    :param offset: (optional)
        The ``(dx, dy)`` offset of the label (in points) from the default
        centered position.

    :param fontsize: (optional)
        The fontsize to use.

    :param plot_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.patches.Ellipse` constructor.

    :param label_param: (optional)
        Default value: None
        FIXME (undocumented)

    :param shape: (optional)
        String in {ellipse (default), rectangle}
        If rectangle, aspect and scale holds for rectangle

    """
    def __init__(self, name, content, x, y, scale=1., aspect=None,
                 observed=False, fixed=False, deterministic=False,
                 offset=[0., 0.], fontsize=None, plot_params={}, label_params=None,
                 shape="ellipse"):
        # Node style.
        assert not (observed and fixed and deterministic), \
            "A node cannot be more than one of 'observed', 'fixed', or 'deterministic'."
        self.observed = observed
        self.fixed = fixed
        self.deterministic = deterministic

        # Metadata.
        self.name = name
        self.content = content

        # Coordinates and dimensions.
        self.x, self.y = float(x), float(y)
        self.scale = float(scale)
        if self.fixed:
            self.scale /= 6.0
        if aspect is not None:
            self.aspect = float(aspect)
        else:
            self.aspect = aspect

        # Set fontsize
        if fontsize is not None:
            self.fontsize = fontsize
        else:
            self.fontsize = mpl.rcParams['font.size']

        # Display parameters.
        self.plot_params = dict(plot_params)

        # Text parameters.
        self.offset = list(offset)
        if label_params is not None:
            self.label_params = dict(label_params)
        else:
            self.label_params = None

        # Shape
        if shape in ["ellipse", "rectangle"]:
            self.shape = shape
        else:
            print("Warning: wrong shape value, set to ellipse instead")
            self.shape = "ellipse"

    def render(self, ctx):
        """
        Render the node.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        # Get the axes and default plotting parameters from the rendering
        # context.
        ax = ctx.ax()

        # Resolve the plotting parameters.
        p = dict(self.plot_params)
        p["lw"] = _pop_multiple(p, ctx.line_width, "lw", "linewidth")

        p["ec"] = p["edgecolor"] = _pop_multiple(p, ctx.node_ec,
                                                 "ec", "edgecolor")

        p["fc"] = _pop_multiple(p, "none", "fc", "facecolor")
        fc = p["fc"]

        p["alpha"] = p.get("alpha", 1)

        # And the label parameters.
        if self.label_params is None:
            l = dict(ctx.label_params)
        else:
            l = dict(self.label_params)

        l["va"] = _pop_multiple(l, "center", "va", "verticalalignment")
        l["ha"] = _pop_multiple(l, "center", "ha", "horizontalalignment")

        # Deal with ``fixed`` nodes.
        scale = self.scale
        if self.fixed:
            # MAGIC: These magic numbers should depend on the grid/node units.
            self.offset[1] += 6

            l["va"] = "baseline"
            l.pop("verticalalignment", None)
            l.pop("ma", None)

            if p["fc"] == "none":
                p["fc"] = "k"

        diameter = ctx.node_unit * scale
        if self.aspect is not None:
            aspect = self.aspect
        else:
            aspect = ctx.aspect

        # Set up an observed node or deterministic node. Note the fc INSANITY.
        if self.observed and not self.fixed:
            style = ctx.observed_style
        elif self.deterministic and not self.fixed:
            style = ctx.deterministic_style
        else:
            style = False

        if style:
            # Update the plotting parameters depending on the style of
            # observed node.
            h = float(diameter)
            w = aspect * float(diameter)
            if style == "shaded":
                p["fc"] = "0.7"
            elif style == "outer":
                h = diameter + 0.1 * diameter
                w = aspect * diameter + 0.1 * diameter
            elif style == "inner":
                h = diameter - 0.1 * diameter
                w = aspect * diameter - 0.1 * diameter
                p["fc"] = fc

            # Draw the background ellipse.
            if self.shape == "ellipse":
                bg = Ellipse(xy=ctx.convert(self.x, self.y),
                             width=w, height=h, **p)
            elif self.shape == "rectangle":
                # Adapt to make Rectangle the same api than ellipse
                wi = w
                xy = ctx.convert(self.x, self.y)
                xy[0] = xy[0] - wi / 2.
                xy[1] = xy[1] - h /2.

                bg = Rectangle(xy=xy, width=wi, height=h, **p)
            else:
                # Should never append
                raise(ValueError("Wrong shape in object causes an error in render"))

            ax.add_artist(bg)

            # Reset the face color.
            p["fc"] = fc

        # Draw the foreground ellipse.
        if style == "inner" and not self.fixed:
            p["fc"] = "none"

        if self.shape == "ellipse":
            el = Ellipse(xy=ctx.convert(self.x, self.y),
                         width=diameter * aspect, height=diameter, **p)
        elif self.shape =="rectangle":
            # Adapt to make Rectangle the same api than ellipse
            wi = diameter * aspect
            xy = ctx.convert(self.x, self.y)
            xy[0] = xy[0] - wi / 2.
            xy[1] = xy[1] - diameter /2.

            el = Rectangle(xy=xy, width=wi, height=diameter, **p)
        else:
            # Should never append
            raise(ValueError("Wrong shape in object causes an error in render"))

        ax.add_artist(el)

        # Reset the face color.
        p["fc"] = fc

        # Annotate the node.
        ax.annotate(self.content, ctx.convert(self.x, self.y),
                    xycoords="data",
                    xytext=self.offset, textcoords="offset points",
                    size=self.fontsize, **l)

        return el

    def get_frontier_coord(self, target_xy, ctx):
        """
        Get the coordinates of the point of intersection between the
        shape of the node and a line starting from the center of the node to an
        arbitrary point. See the example of rectangle bellow:

                    _____________
                    |            |    ____--X (target_node)
                    |        __--X----
                    |     X--    |(return coordinate of this point)
                    |            |
                    |____________|

        :target_xy: (x float, y float)
            A tuple of coordinate of target node
        """

        # Scale the coordinates appropriately.
        x1, y1 = ctx.convert(self.x, self.y)
        x2, y2 = target_xy[0], target_xy[1]

        # Aspect ratios.
        a = self.aspect
        if a is None:
            a = ctx.aspect

        if self.shape == 'ellipse':
            # Compute the distances.
            dx, dy = x2 - x1, y2 - y1
            dist1 = np.sqrt(dy * dy + dx * dx / float(a ** 2))

            # Compute the fractional effect of the radii of the nodes.
            alpha1 = 0.5 * ctx.node_unit * self.scale / dist1

            # Get the coordinates of the starting position.
            x0, y0 = x1 + alpha1 * dx, y1 + alpha1 * dy

            return x0, y0

        elif self.shape == 'rectangle':

            dx, dy = x2 - x1, y2 - y1

            theta = np.angle(complex(dx, dy))
            #print(theta)
            #left or right intersection
            dxx1 = self.scale*a/2.*(np.sign(dx) or 1.)
            dyy1 = self.scale*a/2.*np.abs(dy/dx)*(np.sign(dy) or 1.)
            val1 = np.abs(complex(dxx1, dyy1))

            #up or bottom intersection
            dxx2 =  self.scale*0.5*np.abs(dx/dy)*(np.sign(dx ) or 1.)
            dyy2 =  self.scale*0.5*(np.sign(dy ) or 1.)
            val2 = np.abs(complex(dxx2, dyy2))


            if val1 < val2:
                return x1 + dxx1, y1 + dyy1
            else:
                return x1 + dxx2, y1 + dyy2


        else:
            # Should never append
            raise(ValueError("Wrong shape in object causes an error"))





class Edge(object):
    """
    An edge between two :class:`Node` objects.

    :param node1:
        The first :class:`Node`.

    :param node2:
        The second :class:`Node`. The arrow will point towards this node.

    :param directed: (optional)
        Should the edge be directed from ``node1`` to ``node2``? In other
        words: should it have an arrow?

    :param plot_params: (optional)
        A dictionary of parameters to pass to the plotting command when
        rendering.

    """
    def __init__(self, node1, node2, directed=True,
                 xoffset=0, yoffset=0, plot_params={}):
        self.node1 = node1
        self.node2 = node2
        self.directed = directed
        self.plot_params = dict(plot_params)
        self.xoffset = xoffset
        self.yoffset = yoffset

    def _get_coords(self, ctx):
        """
        Get the coordinates of the line.

        :param conv:
            A callable coordinate conversion.

        :returns:
            * ``x0``, ``y0``: the coordinates of the start of the line.
            * ``dx0``, ``dy0``: the displacement vector.

        """
        # Scale the coordinates appropriately.
        x1, y1 = ctx.convert(self.node1.x, self.node1.y)
        x2, y2 = ctx.convert(self.node2.x, self.node2.y)

        x3, y3 = self.node1.get_frontier_coord((x2, y2), ctx)
        x4, y4 = self.node2.get_frontier_coord((x1, y1), ctx)


        return x3, y3, x4 - x3, y4 - y3

    def render(self, ctx):
        """
        Render the edge in the given axes.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        ax = ctx.ax()

        p = self.plot_params
        p["linewidth"] = _pop_multiple(p, ctx.line_width,
                                       "lw", "linewidth")

        p["linestyle"] = p.get("linestyle", '-')

        # Add edge annotation.
        if "label" in self.plot_params:
            x, y, dx, dy = self._get_coords(ctx)
            ax.annotate(self.plot_params["label"],
                        [x + 0.5 * dx + self.xoffset,
                         y + 0.5 * dy + self.yoffset],
                         xycoords="data",
                        xytext=[0, 3], textcoords="offset points",
                        ha="center", va="center")

        if self.directed:
            p["ec"] = _pop_multiple(p, "k", "ec", "edgecolor")
            p["fc"] = _pop_multiple(p, "k", "fc", "facecolor")
            p["head_length"] = p.get("head_length", 0.25)
            p["head_width"] = p.get("head_width", 0.1)

            # Build an arrow.
            args = self._get_coords(ctx)

            #zero lengh arrow produce error
            if not(args[2] == 0. and args[3] == 0.):
                ar = FancyArrow(*self._get_coords(ctx), width=0,
                    length_includes_head=True, **p)

                # Add the arrow to the axes.
                ax.add_artist(ar)
                return ar

            else:
                print(args[2], args[3] )


        else:
            p["color"] = p.get("color", "k")

            # Get the right coordinates.
            x, y, dx, dy = self._get_coords(ctx)

            # Plot the line.
            line = ax.plot([x, x + dx], [y, y + dy], **p)
            return line


class Plate(object):
    """
    A plate to encapsulate repeated independent processes in the model.

    :param rect:
        The rectangle describing the plate bounds in model coordinates.

    :param label: (optional)
        A string to annotate the plate.

    :param label_offset: (optional)
        The x and y offsets of the label text measured in points.

    :param shift: (optional)
        The vertical "shift" of the plate measured in model units. This will
        move the bottom of the panel by ``shift`` units.

    :param position: (optional)
        One of ``"bottom left"`` or ``"bottom right"``.

    :param fontsize: (optional)
        The fontsize to use.

    :param rect_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.patches.Rectangle` constructor.

    """
    def __init__(self, rect, label=None, label_offset=[5, 5], shift=0,
                 position="bottom left", fontsize=None, rect_params=None, bbox=None):
        self.rect = rect
        self.label = label
        self.label_offset = label_offset
        self.shift = shift
        if fontsize is not None:
            self.fontsize = fontsize
        else:
            self.fontsize = mpl.rcParams['font.size']
        if rect_params is not None:
            self.rect_params = dict(rect_params)
        else:
            self.rect_params = None
        if bbox is not None:
            self.bbox = dict(bbox)
            if not "self.bbox['fc']" in locals():
                self.bbox['fc'] = 'none'
        else:
            self.bbox = None
        self.position = position

    def render(self, ctx):
        """
        Render the plate in the given axes.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        ax = ctx.ax()

        s = np.array([0, self.shift])
        r = np.atleast_1d(self.rect)
        bl = ctx.convert(*(r[:2] + s))
        tr = ctx.convert(*(r[:2] + r[2:]))
        r = np.concatenate([bl, tr - bl])

        if self.rect_params is not None:
            p = self.rect_params
        else:
            p = dict({})

        p["ec"] = _pop_multiple(p, "k", "ec", "edgecolor")
        p["fc"] = _pop_multiple(p, "none", "fc", "facecolor")
        p["lw"] = _pop_multiple(p, ctx.line_width, "lw", "linewidth")
        rect = Rectangle(r[:2], *r[2:], **p)

        ax.add_artist(rect)

        if self.label is not None:
            offset = np.array(self.label_offset)
            if self.position == "bottom left":
                pos = r[:2]
                ha = "left"
            elif self.position == "bottom right":
                pos = r[:2]
                pos[0] += r[2]
                ha = "right"
                offset[0] -= 2 * offset[0]
            else:
                raise RuntimeError("Unknown positioning string: {0}"
                                   .format(self.position))

            ax.annotate(self.label, pos, xycoords="data",
                        xytext=offset, textcoords="offset points",
                        size=self.fontsize, bbox=self.bbox,
                        horizontalalignment=ha)

        return rect


class _rendering_context(object):
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

    :param deterministic_style: (optional)
        How should the "deterministic" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param node_ec:
        The default edge color for the nodes.

    :param directed:
        Should the edges be directed by default?

    :param aspect:
        The default aspect ratio for the nodes.

    :param label_params:
        Default node label parameters.

    """

    def __init__(self, **kwargs):
        # Save the style defaults.
        self.line_width = kwargs.get("line_width", 1.0)

        # Make sure that the observed node style is one that we recognize.
        self.observed_style = kwargs.get("observed_style", "shaded").lower()
        styles = ["shaded", "inner", "outer"]
        assert self.observed_style in styles, \
            "Unrecognized observed node style: {0}\n".format(
                self.observed_style) \
            + "\tOptions are: {0}".format(", ".join(styles))

        # Make sure that the deterministic node style is one that we recognize.
        self.deterministic_style = kwargs.get("deterministic_style", "inner").lower()
        styles = ["shaded", "inner", "outer"]
        assert self.deterministic_style in styles, \
            "Unrecognized deterministic node style: {0}\n".format(
                self.deterministic_style) \
            + "\tOptions are: {0}".format(", ".join(styles))

        # Set up the figure and grid dimensions.
        self.padding = .1
        self.shp_fig_scale = 2.54

        self.shape = np.array(kwargs.get("shape", [1, 1]))
        self.origin = np.array(kwargs.get("origin", [0, 0]))
        self.grid_unit = kwargs.get("grid_unit", 2.0)
        self.figsize = self.grid_unit * self.shape / self.shp_fig_scale

        self.node_unit = kwargs.get("node_unit", 1.0)
        self.node_ec = kwargs.get("node_ec", "k")
        self.directed = kwargs.get("directed", True)
        self.aspect = kwargs.get("aspect", 1.0)
        self.label_params = dict(kwargs.get("label_params", {}))

        self.dpi = kwargs.get('dpi', None)

        # Initialize the figure to ``None`` to handle caching later.
        self._figure = None
        self._ax = None

    def reset_shape(self, shape, adj_origin=False):
        # shape is scaled by grid_unit
        # so divide by grid_unit for proper shape
        self.shape = shape / self.grid_unit + self.padding
        self.figsize = self.grid_unit * self.shape / self.shp_fig_scale

    def reset_origin(self, origin, adj_shape=False):
        # origin is scaled by grid_unit
        # so divide by grid_unit for proper shape
        self.origin = origin / self.grid_unit - self.padding
        if adj_shape:
            self.shape -= self.origin
            self.figsize = self.grid_unit * self.shape / self.shp_fig_scale

    def reset_figure(self):
        if not self._figure is None:
            plt.close(self._figure)
            self._figure = None
            self._ax = None

    def figure(self):
        if self._figure is not None:
            return self._figure
        self._figure = plt.figure(figsize=self.figsize, dpi=self.dpi)
        return self._figure

    def ax(self):
        if self._ax is not None:
            return self._ax

        # Add a new axis object if it doesn't exist.
        self._ax = self.figure().add_axes((0, 0, 1, 1), frameon=False,
                                          xticks=[], yticks=[])

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
        assert len(xy) == 2
        return self.grid_unit * (np.atleast_1d(xy) - self.origin)


def _pop_multiple(d, default, *args):
    """
    A helper function for dealing with the way that matplotlib annoyingly
    allows multiple keyword arguments. For example, ``edgecolor`` and ``ec``
    are generally equivalent but no exception is thrown if they are both
    used.

    *Note: This function does throw a :class:`ValueError` if more than one
    of the equivalent arguments are provided.*

    :param d:
        A :class:`dict`-like object to "pop" from.

    :param default:
        The default value to return if none of the arguments are provided.

    :param *args:
        The arguments to try to retrieve.

    """
    assert len(args) > 0, "You must provide at least one argument to 'pop'."

    results = []
    for k in args:
        try:
            results.append((k, d.pop(k)))
        except KeyError:
            pass

    if len(results) > 1:
        raise TypeError("The arguments ({0}) are equivalent, you can only "
                        .format(", ".join([k for k, v in results]))
                        + "provide one of them.")

    if len(results) == 0:
        return default

    return results[0][1]
