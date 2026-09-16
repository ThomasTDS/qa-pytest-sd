from pytest_bdd import scenarios

from steps.login_steps import *  # noqa: F401, F403
from steps.security_steps import *  # noqa: F401, F403

scenarios("security.feature")
