from pytest_bdd import scenarios

from steps.contact_steps import *  # noqa: F401, F403

scenarios("contact.feature")
