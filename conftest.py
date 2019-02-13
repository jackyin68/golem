from typing import List
import pytest
import _pytest

from scripts.node_integration_tests.tests.base import \
    ReuseNodeKeysCommandLineOption


def pytest_addoption(parser: _pytest.config.Parser) -> None:
    parser.addoption("--runslow", action="store_true",
                     default=False, help="run slow tests")

    parser.addoption("--reuse_keys",
                     help="Parameter setting if provider's and requestor's node"
                          " keys should be reused. Options are: 'yes', 'no'")


def pytest_collection_modifyitems(config: _pytest.config.Config,
                                  items: List[_pytest.main.Item]) -> None:
    if config.getoption("--reuse_keys"):
        reuse_keys_option = config.getvalue("--reuse_keys")
        if reuse_keys_option not in ['yes', 'no']:
            raise Exception("--reuse_keys should be: 'default', 'yes' or 'no'")
        ReuseNodeKeysCommandLineOption(reuse_keys_option)

    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
