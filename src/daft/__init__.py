"""Code for Daft"""

from importlib.metadata import version as get_distribution

from .Plate import Plate, Text

from . import _core, _exceptions, _utils
from ._core import PGM, Node, Edge
from ._exceptions import SameLocationError
from ._utils import _rendering_context, _pop_multiple

__version__ = get_distribution("daft")
__all__ = []
__all__ += _core.__all__
__all__ += node.__all__
__all__ += edge.__all__
__all__ += _exceptions.__all__
__all__ += _utils.__all__
__all__ += _types.__all__
