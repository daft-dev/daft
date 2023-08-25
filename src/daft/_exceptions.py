"""Daft errors"""

__all__: list[str] = []


class SameLocationError(Exception):
    """
    Exception to notify if two nodes are in the same position in the plot.

    :param edge:
        The Edge object whose nodes are being added.
    """

    def __init__(self, edge):
        self.message = (
            "Attempted to add edge between `{}` and `{}` but they "
            + "share the same location."
        ).format(edge.node1.name, edge.node2.name)
        super().__init__(self.message)
