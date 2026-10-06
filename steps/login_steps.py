import os
import uuid

import pytest
from faker import Faker
from pytest_bdd import given, parsers, then, when

from pages.login_page import LoginPage
from pages.register_page import AccountInfo, RegisterPage
from pages.retry import retry_while_failing
from steps.report import add_report_note

fake = Faker("pt_BR")


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
def logout(login_page: LoginPage, request: pytest.FixtureRequest) -> None:
    _, reloads = retry_while_failing(
        first=login_page.logout,
        again=login_page.reload,
        failed=lambda _: not login_page.is_on_login_page(),
    )
    if reloads:
        add_report_note(
            request,
            "Logout: o site não redirecionou para /login e a página foi recarregada "
            f"{reloads} vez(es). Em execuções com WebKit, o servidor respondeu erro (HTTP 520) "
            "para /logout.",
        )


@then("ele deve ver que está deslogado")
def assert_logged_out(login_page: LoginPage) -> None:
    login_page.assert_logged_out()


@when("ele se cadastra com um e-mail novo")
def signup_new_user(
    register_page: RegisterPage,
    created_accounts: list[tuple[str, str]],
    request: pytest.FixtureRequest,
) -> None:
    first_name = fake.first_name()
    last_name = fake.last_name()
    unique_email = f"qa-pytest-sd-{uuid.uuid4().hex}@mailinator.com"
    password = fake.password(length=12, special_chars=False)
    start_retries = register_page.start_signup(f"{first_name} {last_name}", unique_email)
    register_page.fill_account_information(
        AccountInfo(
            password=password,
            first_name=first_name,
            last_name=last_name,
            company=fake.company(),
            address=fake.street_address(),
            state=fake.state(),
            city=fake.city(),
            zipcode=fake.postcode(),
            mobile_number=fake.numerify("##########"),
            country="Canada",
        )
    )
    create_retries = register_page.submit_account_information()
    created_accounts.append((unique_email, password))
    if start_retries or create_retries:
        add_report_note(
            request,
            "Cadastro: o site não avançou na primeira tentativa "
            f"(reenvios: início={start_retries}, criação={create_retries}). "
            "Em execuções com WebKit, interações foram registradas antes de a página estar pronta.",
        )


@then(parsers.parse('ele deve ver a mensagem "{expected_message}"'))
def assert_account_message(register_page: RegisterPage, expected_message: str) -> None:
    register_page.assert_account_created(expected_message)


@then("a conta criada deve poder ser removida")
def delete_created_account(
    register_page: RegisterPage,
    created_accounts: list[tuple[str, str]],
    request: pytest.FixtureRequest,
) -> None:
    register_page.continue_after_account_created()
    delete_retries = register_page.delete_account()
    created_accounts.clear()
    if delete_retries:
        add_report_note(
            request,
            "Remoção da conta: o site respondeu erro na primeira tentativa e a página "
            f"foi recarregada {delete_retries} vez(es).",
        )


@when("ele tenta se cadastrar com o e-mail da conta de teste")
def signup_with_test_user_email(register_page: RegisterPage) -> None:
    email = os.getenv("TEST_USER_EMAIL")
    if not email:
        raise RuntimeError("TEST_USER_EMAIL precisa estar definido (veja .env.example)")
    register_page.submit_signup("QA Pytest SD", email)


@then(parsers.parse('ele deve ver a mensagem de erro de cadastro "{expected_message}"'))
def assert_signup_error(register_page: RegisterPage, expected_message: str) -> None:
    register_page.assert_signup_error(expected_message)
