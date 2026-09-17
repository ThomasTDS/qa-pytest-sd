from pytest_bdd import then, when

from pages.checkout_page import CheckoutPage, PaymentDetails


@when("ele prossegue para o checkout")
def proceed_to_checkout(checkout_page: CheckoutPage) -> None:
    checkout_page.proceed_to_checkout()


@when("ele confirma o pedido")
def place_order(checkout_page: CheckoutPage) -> None:
    checkout_page.place_order()


@when("ele preenche o pagamento com um cartão de teste")
def fill_payment(checkout_page: CheckoutPage) -> None:
    checkout_page.fill_payment(
        PaymentDetails(
            name_on_card="QA Pytest SD",
            card_number="4111111111111111",
            cvc="123",
            expiry_month="12",
            expiry_year="2030",
        )
    )


@then("ele deve ver a confirmação do pedido")
def assert_order_placed(checkout_page: CheckoutPage) -> None:
    checkout_page.assert_order_placed()


@then("ele deve ver a mensagem pedindo para fazer login")
def assert_login_required_message(checkout_page: CheckoutPage) -> None:
    checkout_page.assert_login_required_message()


@then("ele não deve ver a opção de prosseguir para o checkout")
def assert_proceed_to_checkout_not_visible(checkout_page: CheckoutPage) -> None:
    checkout_page.assert_proceed_to_checkout_not_visible()
