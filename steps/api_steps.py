from pytest_bdd import parsers, then

from pages.api_page import ApiPage


@then(parsers.parse('a API de produtos deve conter o produto "{product_name}"'))
def assert_products_list_contains(api_page: ApiPage, product_name: str) -> None:
    api_page.assert_products_list_contains(product_name)


@then("a API de marcas não deve estar vazia")
def assert_brands_list_not_empty(api_page: ApiPage) -> None:
    api_page.assert_brands_list_not_empty()


@then(parsers.parse('a busca via API por "{term}" deve retornar o produto "{product_name}"'))
def assert_search_results_contain(api_page: ApiPage, term: str, product_name: str) -> None:
    api_page.assert_search_results_contain(term, product_name)


@then("a API de produtos deve rejeitar POST com o código 405")
def assert_products_list_rejects_post(api_page: ApiPage) -> None:
    api_page.assert_products_list_rejects_post()


@then("a verificação de login via API com a conta de teste deve confirmar que o usuário existe")
def assert_verify_login_succeeds_for_test_user(api_page: ApiPage) -> None:
    api_page.assert_verify_login_succeeds_for_test_user()


@then(
    parsers.parse(
        'a verificação de login via API com o e-mail "{email}" e a senha "{password}" '
        "deve indicar que o usuário não foi encontrado"
    )
)
def assert_verify_login_fails(api_page: ApiPage, email: str, password: str) -> None:
    api_page.assert_verify_login_fails(email, password)


@then("a API deve permitir criar e remover uma conta")
def assert_create_and_delete_account_roundtrip(api_page: ApiPage) -> None:
    api_page.assert_create_and_delete_account_roundtrip()


@then("a consulta de detalhes do usuário de teste via API deve retornar o seu perfil")
def assert_user_detail_by_email_for_test_user(api_page: ApiPage) -> None:
    api_page.assert_user_detail_by_email_for_test_user()
