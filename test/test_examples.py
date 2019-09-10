import os
import sys
import importlib
import daft
import matplotlib as mpl

mpl.rcParams["figure.max_open_warning"] = 100

OUTPUT_FIGS = False

SAVEFIG = daft.PGM.savefig


def test_savefig(*args, **kwargs):
    return


def get_examples(folder):
    examples = []
    for file in os.listdir(folder):
        file_name, ext = os.path.splitext(file)
        if ext == ".py":
            examples.append(file_name)
    return examples


def run_examples(examples, test_figs=False):
    if test_figs:
        daft.PGM.savefig = SAVEFIG
    else:
        daft.PGM.savefig = test_savefig
    for file in examples:
        print("Testing {0}.py".format(file))
        _ = importlib.import_module("examples." + file)


def remove_imgs(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except os.error:
                print("Could not unlink {0}".format(file))


# if __name__ == '__main__':
this_path = os.path.dirname(os.path.abspath(__file__))
daft_path = os.path.abspath(os.path.join(this_path, ".."))
sys.path.insert(0, daft_path)

if OUTPUT_FIGS:
    img_path = os.path.abspath(os.path.join(daft_path, "test/imgs"))
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    os.chdir(img_path)

print("\nExecuting examples...\n")
examples = get_examples(os.path.abspath(os.path.join(daft_path, "examples")))
run_examples(examples=examples, test_figs=OUTPUT_FIGS)

if OUTPUT_FIGS:
    remove_imgs(img_path)
    print("\nDeleting all images...\n")
    os.chdir(this_path)
    try:
        os.rmdir(img_path)
    except os.error:
        print("Could not remove {0}".format(img_path))
