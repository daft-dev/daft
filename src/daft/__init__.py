"""Code for Daft"""

from importlib.metadata import version as get_distribution

from . import exceptions, node, edge, pgm, plate, types, utils
from .pgm import PGM
from .node import Node
from .edge import Edge
from .plate import Plate, Text
from .exceptions import SameLocationError
from .utils import RenderingContext, _pop_multiple

__version__ = get_distribution("daft-pgm")
__all__ = []
__all__ += pgm.__all__
__all__ += node.__all__
__all__ += edge.__all__
__all__ += plate.__all__
__all__ += exceptions.__all__
__all__ += utils.__all__
__all__ += types.__all__
