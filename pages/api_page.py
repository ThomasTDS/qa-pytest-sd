import os
import uuid

from faker import Faker
from playwright.sync_api import APIResponse, Page

TEST_ACCOUNT_PASSWORD = "SenhaDeTeste123"
fake = Faker("pt_BR")


class ApiPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def _get_products_list(self) -> APIResponse:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        return self.page.request.get(base_url + "api/productsList")

    def _get_brands_list(self) -> APIResponse:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        return self.page.request.get(base_url + "api/brandsList")

    def _search_products(self, term: str) -> APIResponse:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        return self.page.request.post(base_url + "api/searchProduct", form={"search_product": term})

    def assert_products_list_contains(self, product_name: str) -> None:
        response = self._get_products_list()
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert any(product["name"] == product_name for product in body["products"])

    def assert_brands_list_not_empty(self) -> None:
        response = self._get_brands_list()
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert isinstance(body["brands"], list)
        assert len(body["brands"]) > 0

    def assert_search_results_contain(self, term: str, product_name: str) -> None:
        response = self._search_products(term)
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert any(product["name"] == product_name for product in body["products"])

    def assert_products_list_rejects_post(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        response = self.page.request.post(base_url + "api/productsList")
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 405

    def assert_verify_login_succeeds_for_test_user(self) -> None:
        email = os.getenv("TEST_USER_EMAIL")
        password = os.getenv("TEST_USER_PASSWORD")
        if not email or not password:
            raise RuntimeError(
                "TEST_USER_EMAIL e TEST_USER_PASSWORD precisam estar definidos (veja .env.example)"
            )
        self.assert_verify_login_succeeds(email, password)

    def assert_verify_login_succeeds(self, email: str, password: str) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        response = self.page.request.post(
            base_url + "api/verifyLogin", form={"email": email, "password": password}
        )
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert body["message"] == "User exists!"

    def assert_verify_login_fails(self, email: str, password: str) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        response = self.page.request.post(
            base_url + "api/verifyLogin", form={"email": email, "password": password}
        )
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 404
        assert body["message"] == "User not found!"

    def create_account(self, email: str) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        response = self.page.request.post(
            base_url + "api/createAccount",
            form={
                "name": fake.first_name(),
                "email": email,
                "password": TEST_ACCOUNT_PASSWORD,
                "title": "Mr",
                "birth_date": "10",
                "birth_month": "5",
                "birth_year": "1995",
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "company": fake.company(),
                "address1": fake.street_address(),
                "address2": "",
                "country": "Canada",
                "zipcode": fake.postcode(),
                "state": fake.state(),
                "city": fake.city(),
                "mobile_number": fake.numerify("##########"),
            },
        )
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 201

    def delete_account(self, email: str, password: str = TEST_ACCOUNT_PASSWORD) -> None:
        response = self._request_delete_account(email, password)
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200

    def try_delete_account(self, email: str, password: str) -> bool:
        response = self._request_delete_account(email, password)
        return response.status == 200 and response.json()["responseCode"] == 200

    def _request_delete_account(self, email: str, password: str) -> APIResponse:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        return self.page.request.delete(
            base_url + "api/deleteAccount",
            form={"email": email, "password": password},
        )

    def assert_create_and_delete_account_roundtrip(self) -> None:
        email = f"qa-pytest-sd-{uuid.uuid4().hex}@mailinator.com"
        self.create_account(email)
        self.delete_account(email)

    def assert_user_detail_by_email_for_test_user(self) -> None:
        email = os.getenv("TEST_USER_EMAIL")
        if not email:
            raise RuntimeError("TEST_USER_EMAIL precisa estar definido (veja .env.example)")
        self.assert_user_detail_by_email(email)

    def assert_user_detail_by_email(self, email: str) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        response = self.page.request.get(base_url + "api/getUserDetailByEmail?email=" + email)
        assert response.status == 200
        body = response.json()
        assert body["responseCode"] == 200
        assert body["user"]["email"].lower() == email.lower()
