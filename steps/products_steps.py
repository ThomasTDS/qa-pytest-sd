from pytest_bdd import given, parsers, then, when

from pages.cart_page import CartPage
from pages.products_page import ProductsPage


@given("que o usuário está na página de produtos")
@when("que o usuário está na página de produtos")
def go_to_products(products_page: ProductsPage) -> None:
    products_page.goto()


@when(parsers.parse('ele busca por "{term}"'))
def search_products(products_page: ProductsPage, term: str) -> None:
    products_page.search(term)


@then("ele deve ver resultados da busca")
def assert_search_results_visible(products_page: ProductsPage) -> None:
    products_page.assert_search_results_visible()


@when(parsers.parse('ele adiciona os produtos "{product1}" e "{product2}" ao carrinho'))
def add_two_products_to_cart(products_page: ProductsPage, product1: str, product2: str) -> None:
    products_page.add_product_to_cart(product1)
    products_page.add_product_to_cart(product2)


@when(parsers.parse('ele adiciona o produto "{product_name}" ao carrinho'))
def add_product_to_cart(products_page: ProductsPage, product_name: str) -> None:
    products_page.add_product_to_cart(product_name)


@when("ele acessa o carrinho")
def go_to_cart(cart_page: CartPage) -> None:
    cart_page.goto()


@then(parsers.parse('ele deve ver os produtos "{product1}" e "{product2}" no carrinho'))
def assert_two_products_in_cart(cart_page: CartPage, product1: str, product2: str) -> None:
    cart_page.assert_product_in_cart(product1)
    cart_page.assert_product_in_cart(product2)


@when(parsers.parse('ele remove o produto "{product_name}" do carrinho'))
def remove_product_from_cart(cart_page: CartPage, product_name: str) -> None:
    cart_page.remove_product(product_name)


@then(parsers.parse('ele não deve ver o produto "{product_name}" no carrinho'))
def assert_product_not_in_cart(cart_page: CartPage, product_name: str) -> None:
    cart_page.assert_product_not_in_cart(product_name)


@then(parsers.parse('ele deve ver o produto "{product_name}" no carrinho'))
def assert_product_in_cart(cart_page: CartPage, product_name: str) -> None:
    cart_page.assert_product_in_cart(product_name)
