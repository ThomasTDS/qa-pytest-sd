import os
import uuid

from pytest_bdd import given, parsers, then, when

from pages.login_page import LoginPage
from pages.register_page import AccountInfo, RegisterPage


@given("que o usuário está na página de login")
def go_to_login(login_page: LoginPage) -> None:
    login_page.goto()


@when("ele faz login com a conta de teste")
def login_with_test_user(login_page: LoginPage) -> None:
    login_page.login_with_test_user()


@when(parsers.parse('ele insere o e-mail "{email}" e a senha "{password}"'))
def login_with_credentials(login_page: LoginPage, email: str, password: str) -> None:
    login_page.login(email, password)


@then("ele deve ver que está logado")
def assert_logged_in(login_page: LoginPage) -> None:
    login_page.assert_logged_in()


@then(parsers.parse('ele deve ver a mensagem de erro "{expected_message}"'))
def assert_error_message(login_page: LoginPage, expected_message: str) -> None:
    login_page.assert_error_message(expected_message)


@when("ele faz logout")
def logout(login_page: LoginPage) -> None:
    login_page.logout()


@then("ele deve ver que está deslogado")
def assert_logged_out(login_page: LoginPage) -> None:
    login_page.assert_logged_out()


@when("ele se cadastra com um e-mail novo")
def signup_new_user(register_page: RegisterPage) -> None:
    unique_email = f"qa-pytest-sd-{uuid.uuid4().hex}@mailinator.com"
    register_page.start_signup("QA Pytest SD", unique_email)
    register_page.fill_account_information(
        AccountInfo(
            password="SenhaDeTeste123",
            first_name="QA",
            last_name="Pytest",
            company="qa-pytest-sd",
            address="Rua de Teste, 123",
            state="SP",
            city="Sao Paulo",
            zipcode="01000-000",
            mobile_number="11999999999",
            country="Canada",
        )
    )


@then(parsers.parse('ele deve ver a mensagem "{expected_message}"'))
def assert_account_message(register_page: RegisterPage, expected_message: str) -> None:
    register_page.assert_account_created(expected_message)


@then("a conta criada deve poder ser removida")
def delete_created_account(register_page: RegisterPage) -> None:
    register_page.continue_after_account_created()
    register_page.delete_account()


@when("ele tenta se cadastrar com o e-mail da conta de teste")
def signup_with_test_user_email(register_page: RegisterPage) -> None:
    email = os.getenv("TEST_USER_EMAIL")
    if not email:
        raise RuntimeError("TEST_USER_EMAIL precisa estar definido (veja .env.example)")
    register_page.submit_signup("QA Pytest SD", email)


@then(parsers.parse('ele deve ver a mensagem de erro de cadastro "{expected_message}"'))
def assert_signup_error(register_page: RegisterPage, expected_message: str) -> None:
    register_page.assert_signup_error(expected_message)
