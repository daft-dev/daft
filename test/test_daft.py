import daft
import pytest


def test_auto_size():
    with daft.PGM() as pgm:
        pgm.add_node("node1", x=0.0, y=0.0)
        pgm.add_node("node2", x=1.0, y=0.0)
        pgm.add_edge("node1", "node2")
        pgm.render()


def test_manual_size():
    with daft.PGM(shape=[1, 1], origin=[0, 0]) as pgm:
        pgm.add_node("node1", x=0.0, y=0.0)
        pgm.add_node("node2", x=1.0, y=0.0)
        pgm.add_edge("node1", "node2")
        pgm.render()


def test_add_node():
    with daft.PGM() as pgm:
        pgm.add_node(node="node1", content="content1")
        assert "node1" in pgm._nodes
        assert pgm._nodes["node1"].content == "content1"


def test_add_node_class():
    with daft.PGM() as pgm:
        node = daft.Node(name="node2", content="node2", x=0, y=0)
        pgm.add_node(node)
        assert "node2" in pgm._nodes


def test_overlap_nodes():
    with daft.PGM() as pgm:
        pgm.add_node("node1", x=0, y=0)
        pgm.add_node("node2", x=0, y=0)
        pgm.add_edge("node1", "node2")
        with pytest.raises(daft.SameLocationError):
            pgm.render()


def test_add_edge():
    with daft.PGM() as pgm:
        pgm.add_node("node1")
        pgm.add_node("node2")
        pgm.add_edge(name1="node1", name2="node2")

        edge = pgm._edges[0]
        assert edge.node1 == pgm._nodes["node1"]
        assert edge.node2 == pgm._nodes["node2"]


def test_add_plate():
    with daft.PGM() as pgm:
        pgm.add_plate([0, 0, 1, 1])
        assert pgm._plates[0].rect == [0, 0, 1, 1]


def test_add_text():
    with daft.PGM() as pgm:
        pgm.add_text(x=0, y=0, label="text1")

        plate = pgm._plates[0]
        assert plate.rect == [0, 0, 0, 0]
        assert plate.label == "text1"


def test_pop_multiple():
    _dict = {"ec": "none", "edgecolor": "none"}
    with pytest.raises(TypeError):
        daft._pop_multiple(_dict, "none", "ec", "edgecolor")
