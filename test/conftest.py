import matplotlib
from matplotlib.testing.conftest import *  # noqa


def pytest_configure(config):
    for key, value in [
        ("markers", "flaky: (Provided by pytest-rerunfailures.)"),
        ("markers", "timeout: (Provided by pytest-timeout.)"),
        ("markers", "backend: Set alternate Matplotlib backend temporarily."),
        ("markers", "style: Set alternate Matplotlib style temporarily."),
        ("markers", "baseline_images: Compare output against references."),
        ("markers", "pytz: Tests that require pytz to be installed."),
    ]:
        config.addinivalue_line(key, value)

    matplotlib.use("agg", force=True)
    matplotlib._called_from_pytest = True
    matplotlib._init_tests()
