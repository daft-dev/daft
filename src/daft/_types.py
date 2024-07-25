"""Daft types"""

__all__: list[str] = []

import numpy as np
from numpy.typing import NDArray, ArrayLike
from typing import Any, Annotated, Literal, TypeVar

DType = TypeVar("DType", bound=np.generic)

NDArray2 = Annotated[NDArray[DType], Literal[2]]

NDArrayF = NDArray[np.float64]
NDArrayI = NDArray[np.int64]
