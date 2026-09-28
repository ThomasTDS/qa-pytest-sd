from pytest_bdd import scenarios

from steps.accessibility_steps import *  # noqa: F401, F403
from steps.login_steps import *  # noqa: F401, F403
from steps.products_steps import *  # noqa: F401, F403

scenarios("accessibility.feature")
