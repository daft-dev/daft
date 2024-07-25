"""Daft errors"""

__all__: list[str] = []


import matplotlib as mpl
from matplotlib.patches import Rectangle

import numpy as np

from typing import Any, cast

from .utils import _pop_multiple, RenderingContext
from .types import Tuple2F, Tuple4F, Position, RectParams


class Plate:
    """
    A plate to encapsulate repeated independent processes in the model.

    :param rect:
        The rectangle describing the plate bounds in model coordinates.
        This is [x-start, y-start, x-length, y-length].

    :param label: (optional)
        A string to annotate the plate.

    :param label_offset: (optional)
        The x- and y- offsets of the label text measured in points.

    :param shift: (optional)
        The vertical "shift" of the plate measured in model units. This will
        move the bottom of the panel by ``shift`` units.

    :param position: (optional)
        One of ``"{vertical} {horizontal}"`` where vertical is ``"bottom"``
        or ``"middle"`` or ``"top"`` and horizontal is ``"left"`` or
        ``"center"`` or ``"right"``.

    :param fontsize: (optional)
        The fontsize to use.

    :param rect_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.patches.Rectangle` constructor, which defines
        the properties of the plate.

    :param bbox: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.axes.Axes.annotate` constructor, which defines
        the box drawn around the text.

    """

    def __init__(
        self,
        rect: Tuple4F,
        label: str | None = None,
        label_offset: Tuple2F = (5, 5),
        shift: float = 0,
        position: Position = "bottom left",
        fontsize: float | None = None,
        rect_params: RectParams | None = None,
        bbox: dict[str, Any] | None = None,
    ) -> None:
        self.rect = rect
        self.label = label
        self.label_offset = label_offset
        self.shift = shift

        if fontsize is not None:
            self.fontsize: float | None = fontsize
        else:
            self.fontsize = mpl.rcParams["font.size"]

        if rect_params is not None:
            self.rect_params: RectParams | None = rect_params
        else:
            self.rect_params = None

        if bbox is not None:
            self.bbox: dict[str, Any] | None = dict(bbox)

            # Set the awful default blue color to transparent
            if "fc" not in self.bbox.keys():
                self.bbox["fc"] = "none"
        else:
            self.bbox = None

        self.position = position

    def render(self, ctx: RenderingContext) -> Rectangle:
        """
        Render the plate in the given axes.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        ax = ctx.ax()

        shift = np.array([0, self.shift], dtype=np.float64)
        rect = np.atleast_1d(np.asarray(self.rect, dtype=np.float64))
        bottom_left = np.asarray(
            ctx.convert(*(rect[:2] + shift)), dtype=np.float64
        )
        top_right = np.asarray(
            ctx.convert(*(rect[:2] + rect[2:])), dtype=np.float64
        )
        rect = np.concatenate([bottom_left, top_right - bottom_left])

        if self.rect_params is not None:
            rect_params = self.rect_params
        else:
            rect_params = {}

        rect_params["ec"] = _pop_multiple(rect_params, "k", "ec", "edgecolor")
        rect_params["fc"] = _pop_multiple(
            rect_params, ctx.plate_fc, "fc", "facecolor"
        )
        rect_params["lw"] = _pop_multiple(
            rect_params, ctx.line_width, "lw", "linewidth"
        )

        rectangle = Rectangle(
            xy=(rect[0], rect[1]), width=rect[2], height=rect[3], **rect_params
        )

        ax.add_artist(rectangle)

        if self.label is not None:
            offset = np.array(self.label_offset, dtype=np.float64)
            if "left" in self.position:
                position = rect[:2]
                ha = "left"
            elif "right" in self.position:
                position = rect[:2]
                position[0] += rect[2]
                ha = "right"
                offset[0] = -offset[0]
            elif "center" in self.position:
                position = rect[:2]
                position[0] = rect[2] / 2 + rect[0]
                ha = "center"
            else:
                raise RuntimeError(
                    f"Unknown positioning string: {self.position}"
                )

            if "bottom" in self.position:
                va = "bottom"
            elif "top" in self.position:
                position[1] = rect[1] + rect[3]
                offset[1] = -offset[1] - 0.1
                va = "top"
            elif "middle" in self.position:
                position[1] += rect[3] / 2
                va = "center"
            else:
                raise RuntimeError(
                    f"Unknown positioning string: {self.position}"
                )

            posx, posy = position
            offx, offy = offset

            ax.annotate(
                self.label,
                xy=(posx, posy),
                xycoords="data",
                xytext=(offx, offy),
                textcoords="offset points",
                size=self.fontsize,
                bbox=self.bbox,
                horizontalalignment=ha,
                verticalalignment=va,
            )

        return rectangle


class Text(Plate):
    """
    A subclass of plate to writing text using grid coordinates. Any **kwargs
    are passed through to :class:`PGM.Plate`.

    :param x:
        The x-coordinate of the text in *model units*.

    :param y:
        The y-coordinate of the text.

    :param label:
        A string to write.

    :param fontsize: (optional)
        The fontsize to use.

    """

    def __init__(
        self, x: float, y: float, label: str, fontsize: float | None = None
    ) -> None:
        self.rect = (x, y, 0.0, 0.0)
        self.label = label
        self.fontsize = fontsize
        self.label_offset = (0.0, 0.0)
        self.rect_params = cast(RectParams, {"ec": "none"})
        self.bbox = {"fc": "none", "ec": "none"}

        super().__init__(
            rect=self.rect,
            label=self.label,
            label_offset=self.label_offset,
            fontsize=self.fontsize,
            rect_params=self.rect_params,
            bbox=self.bbox,
        )
