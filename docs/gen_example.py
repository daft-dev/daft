#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import json
from subprocess import check_call


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


def main(file_name, thumb_info):
    # Read each file
    full_path = os.path.join(example_dir, file_name + ".py")
    with open(full_path) as f:
        src = f.read()
    print("Executing: " + full_path)

    # Set up namespace and execute as script
    namespace = globals()
    namespace["pgm"] = None
    exec(src, None, namespace)
    pgm = namespace["pgm"]

    # Generate the RST source file.
    src = src.split("\n")
    if namespace["__doc__"] is None:
        title = file_name.title() + "\n" + "=" * len(file_name)
        doc = ""
    else:
        doc = namespace["__doc__"].split("\n")
        title = "\n".join(doc[:3])
        doc = "\n".join(doc)
        src = src[len(namespace["__doc__"].split("\n")) :]

    fmt_src = "\n".join(["    " + l for l in src])
    img_path = os.path.join(img_out_dir, file_name + ".png")
    thumb_path = os.path.join(img_out_dir, file_name + "-thumb.png")

    rst = example_template.format(
        title=title, doc=doc, example=file_name, src=fmt_src, img_path=img_path
    )

    # Write the RST file.
    rstfn = os.path.join(out_dir, file_name + ".rst")
    print("Writing: " + rstfn)
    with open(rstfn, "w") as f:
        f.write(rst)

    # Remove the generated plots.
    for file_ext in [".png", ".pdf", ".svg"]:
        try:
            os.remove(file_name + file_ext)
        except os.error:
            pass

    # Save the new figure.
    print("Saving: " + img_path)
    if file_name == "astronomy":
        dpi = 75
    else:
        dpi = 150
    pgm.savefig(img_path, dpi=dpi)

    # Crop the thumbnail using ImageMagick command-line tool
    # https://imagemagick.org/script/command-line-options.php#crop
    cmd = " ".join(
        ["convert", "-crop 190x190^+{0[0]:d}+{0[1]:d}".format(thumb_info), img_path, thumb_path]
    )
    print(cmd)
    check_call(cmd, shell=True)

    if file_name == "astronomy":
        dpi = 150
    pgm.savefig(img_path, dpi=dpi)


if __name__ == "__main__":
    figs = json.load(open(os.path.join(this_path, "_static", "examples.json")))
    if len(sys.argv) == 1:
        # Build all the examples.
        argv = figs.keys()
    else:
        argv = sys.argv[1:]

    for fig_name in argv:
        assert fig_name in figs, "Add {0} to _static/examples.json".format(fig_name)
        main(fig_name, figs[fig_name])
