from pytest_bdd import scenarios

from steps.products_steps import *  # noqa: F401, F403

scenarios("products.feature")
