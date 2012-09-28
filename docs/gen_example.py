#!/usr/bin/env python

from __future__ import print_function

import os
import sys


this_path = os.path.dirname(os.path.abspath(__file__))
daft_path = os.path.dirname(this_path)
sys.path.insert(0, daft_path)

example_dir = os.path.join(daft_path, "examples")
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
img_out_dir = os.path.join(this_path, "_static", "examples")

try:
    os.makedirs(out_dir)
except os.error:
    pass

try:
    os.makedirs(img_out_dir)
except os.error:
    pass

example_template = """.. _{example}:

{title}

.. figure:: /_static/examples/{example}.png

{doc}

::

{src}

"""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to provide an example name")
        sys.exit(1)

    fn = sys.argv[1]

    # Run the code.
    src = open(os.path.join(example_dir, fn + ".py")).read()
    exec src

    # Generate the RST source file.
    src = src.split("\n")
    if __doc__ is None:
        title = fn.title() + "\n" + "=" * len(fn)
        doc = ""
    else:
        doc = __doc__.split("\n")
        title = "\n".join(doc[:3])
        doc = "\n".join(doc)
        src = src[len(__doc__.split("\n")):]

    fmt_src = "\n".join(["    " + l for l in src])
    img_path = os.path.join(img_out_dir, fn + ".png")

    rst = example_template.format(title=title, doc=doc, example=fn,
            src=fmt_src, img_path=img_path)

    # Write the RST file.
    with open(os.path.join(out_dir, fn + ".rst"), "w") as f:
        f.write(rst)

    # Remove the generated plots.
    try:
        os.remove(fn + ".png")
    except os.error:
        pass
    try:
        os.remove(fn + ".pdf")
    except os.error:
        pass

    # Save the new figure.
    pgm.figure.savefig(img_path, dpi=150)
