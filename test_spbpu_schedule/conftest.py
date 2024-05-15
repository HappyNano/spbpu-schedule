import pathlib


pytest_plugins = ['test_spbpu_schedule.pytest_plugins']

STATIC_PATH = [
    pathlib.Path(__file__).parent / 'static'
]
