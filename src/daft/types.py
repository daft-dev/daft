"""Daft types"""

__all__: list[str] = []

import numpy as np
from numpy.typing import NDArray, ArrayLike
from typing import Any, Annotated, Literal, TypeVar, TypedDict, Optional, Union

T = TypeVar("T")

NDArrayF = NDArray[np.float64]
NDArrayI = NDArray[np.int64]

# Tuple2 = tuple[T, T] | list[T]
Tuple2 = tuple[T, T]
Tuple4 = tuple[T, T, T, T]

Tuple2F = Tuple2[float]
Tuple4F = Tuple4[float]

Shape = Literal["ellipse", "rectangle"]

Position = Literal[
    "bottom left",
    "bottom center",
    "bottom right",
    "middle left",
    "middle center",
    "middle right",
    "top left",
    "top center",
    "top right",
]


class PlotParams(TypedDict):
    lw: str
    linewidth: str
    ec: str
    edgecolor: str
    fc: str
    facecolor: str
    alpha: float


class LabelParams(TypedDict):
    va: str
    verticalalignment: str
    ha: str
    horizontalalignment: str
    ma: str


class RectParams(TypedDict, total=False):
    ec: str
    edgecolor: str
    fc: str
    facecolor: str
    lw: str
    linewidth: str


class CTX_Kwargs(TypedDict):
    shape: NDArrayF
    origin: NDArrayF
    grid_unit: float
    node_unit: float
    observed_style: str
    alternate_style: str
    line_width: float
    node_ec: str
    node_fc: str
    plate_fc: str
    directed: bool
    aspect: float
    label_params: Optional[LabelParams]
    dpi: Optional[int]


AnyDict = Union[dict[str, Any], PlotParams, LabelParams, RectParams, CTX_Kwargs]
