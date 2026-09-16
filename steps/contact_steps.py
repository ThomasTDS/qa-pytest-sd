from pytest_bdd import given, parsers, then, when

from pages.contact_page import ContactPage


@given("que o usuário está na página de contato")
def go_to_contact(contact_page: ContactPage) -> None:
    contact_page.goto()


@given("que o usuário está na página inicial")
def go_to_home(contact_page: ContactPage) -> None:
    contact_page.goto_home()


@when(
    parsers.parse(
        'ele envia o formulário de contato com "{name}", "{email}", "{subject}" e "{message}"'
    )
)
def submit_contact_form(
    contact_page: ContactPage, name: str, email: str, subject: str, message: str
) -> None:
    contact_page.submit_form(name, email, subject, message)


@then("ele deve ver a confirmação de envio do formulário")
def assert_message_sent(contact_page: ContactPage) -> None:
    contact_page.assert_message_sent()


@when(parsers.parse('ele se inscreve na newsletter com o e-mail "{email}"'))
def subscribe_to_newsletter(contact_page: ContactPage, email: str) -> None:
    contact_page.subscribe_to_newsletter(email)


@then("ele deve ver a confirmação da inscrição")
def assert_subscribed(contact_page: ContactPage) -> None:
    contact_page.assert_subscribed()
