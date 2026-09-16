from pytest_bdd import scenarios

from steps.checkout_steps import *  # noqa: F401, F403
from steps.login_steps import *  # noqa: F401, F403
from steps.products_steps import *  # noqa: F401, F403

scenarios("checkout.feature")
