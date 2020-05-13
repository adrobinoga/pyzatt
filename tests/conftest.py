import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--platform", action="store", default="hardware",
        help="simulator|hardware: chose to simulate or use real hardware "
             "(default hardware)"
    )
    parser.addoption(
        "--ip-address", action="store",
        help="ip address of the device, required if platform=hardware"
    )
    parser.addoption(
        "--seed", type=int,
        help="random seed to run tests (not supported yet)"
    )


@pytest.fixture
def parse_options(request):
    opts = {}
    opts['platform'] = request.config.getoption("--platform")
    opts['ip-address'] = request.config.getoption("--ip-address")
    opts['seed'] = request.config.getoption("--seed")

    if opts['platform'] == 'simulator':
        return opts
    else:
        # ip address must exist when using real hardware
        if opts['ip-address']:
            return opts
        else:
            print("IP address must be defined when using real hardware")
            return None
