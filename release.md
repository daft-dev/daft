Steps to perform when doing a release:

1. Bump version number and update changelog date in `HISTORY.rst`
2. `python setup.py sdist` then `pip install dist/whatever` to test
3. Tag a GitHub release
4. `python setup.py sdist` then `twine upload dist/whatever`