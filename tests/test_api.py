from pytest_bdd import scenarios

from steps.api_steps import *  # noqa: F401, F403

scenarios("api.feature")
