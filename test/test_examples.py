import os
import sys
import importlib
import daft

OUTPUT_FIGS = False

EXAMPLES = [
    'astronomy',
    'badfont',
    'bca',
    'classic',
    'deconvolution',
    'exoplanets',
    'fixed',
    'gaia',
    'galex',
    'huey_p_newton',
    'logo',
    'mrf',
    'nocircles',
    'nogray',
    'recursive',
    'thicklines',
    'weaklensing',
    'wordy',
    'yike'
]

savefig = daft.PGM.savefig


def test_savefig(*args, **kwargs):
    return


def test_examples(test_figs=False):
    if test_figs:
        daft.PGM.savefig = savefig
    else:
        daft.PGM.savefig = test_savefig
    for file in EXAMPLES:
        print('Testing {0}.py'.format(file))
        _ = importlib.import_module('examples.' + file)


def remove_imgs(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except os.error:
                pass


if __name__ == '__main__':
    this_path = os.path.dirname(os.path.abspath(__file__))
    daft_path = os.path.abspath(os.path.join(this_path + '/..'))
    sys.path.insert(0, daft_path)

    if OUTPUT_FIGS:
        img_path = os.path.abspath(os.path.join(daft_path, 'test/imgs'))
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        os.chdir(img_path)

    print('\nExecuting examples...\n')
    test_examples(test_figs=OUTPUT_FIGS)

    if OUTPUT_FIGS:
        print('\nDeleting all images...\n')
        remove_imgs(img_path)
        os.chdir(this_path)
        try:
            os.rmdir(img_path)
        except os.error:
            pass
