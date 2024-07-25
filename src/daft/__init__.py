"""Code for Daft"""

from importlib.metadata import version as get_distribution

from . import node, edge, pgm, plate, _exceptions, _utils, _types
from .pgm import PGM
from .node import Node
from .edge import Edge
from .plate import Plate, Text
from ._exceptions import SameLocationError
from ._utils import _RenderingContext, _pop_multiple

__version__ = get_distribution("daft")
__all__ = []
__all__ += pgm.__all__
__all__ += node.__all__
__all__ += edge.__all__
__all__ += plate.__all__
__all__ += _exceptions.__all__
__all__ += _utils.__all__
__all__ += _types.__all__
