from pytest_bdd import then

from pages.security_page import SecurityPage


@then("a aplicação deve responder com os cabeçalhos de segurança esperados")
def assert_security_headers_present(security_page: SecurityPage) -> None:
    security_page.assert_security_headers_present()


@then("o acesso via HTTP deve ser redirecionado para HTTPS")
def assert_http_redirects_to_https(security_page: SecurityPage) -> None:
    security_page.assert_http_redirects_to_https()


@then("o campo de senha deve ser do tipo password")
def assert_password_field_is_masked(security_page: SecurityPage) -> None:
    security_page.assert_password_field_is_masked()


@then("o cookie de sessão deve ter a flag HttpOnly ativada")
def assert_session_cookie_is_http_only(security_page: SecurityPage) -> None:
    security_page.assert_session_cookie_is_http_only()
