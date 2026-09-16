from dataclasses import dataclass

from playwright.sync_api import Page, expect


@dataclass
class AccountInfo:
    password: str
    first_name: str
    last_name: str
    company: str
    address: str
    state: str
    city: str
    zipcode: str
    mobile_number: str
    country: str | None = None


class RegisterPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def start_signup(self, name: str, email: str) -> None:
        self.page.locator('[data-qa="signup-name"]').fill(name)
        self.page.locator('[data-qa="signup-email"]').fill(email)
        self.page.locator('[data-qa="signup-button"]').click()
        expect(self.page.get_by_text("Enter Account Information")).to_be_visible()

    def fill_account_information(self, info: AccountInfo) -> None:
        self.page.locator("#id_gender1").check()
        self.page.locator('[data-qa="password"]').fill(info.password)
        self.page.locator("#days").select_option("10")
        self.page.locator("#months").select_option("5")
        self.page.locator("#years").select_option("1995")

        self.page.locator('[data-qa="first_name"]').fill(info.first_name)
        self.page.locator('[data-qa="last_name"]').fill(info.last_name)
        self.page.locator('[data-qa="company"]').fill(info.company)
        self.page.locator('[data-qa="address"]').fill(info.address)
        self.page.locator('[data-qa="state"]').fill(info.state)
        self.page.locator('[data-qa="city"]').fill(info.city)
        self.page.locator('[data-qa="zipcode"]').fill(info.zipcode)
        self.page.locator('[data-qa="mobile_number"]').fill(info.mobile_number)
        if info.country:
            self.page.locator('[data-qa="country"]').select_option(info.country)

        self.page.locator('[data-qa="create-account"]').click()

    def assert_account_created(self, expected_message: str) -> None:
        expect(self.page.get_by_text(expected_message)).to_be_visible()

    def continue_after_account_created(self) -> None:
        self.page.locator('[data-qa="continue-button"]').click()

    def delete_account(self) -> None:
        self.page.locator('a[href="/delete_account"]').click()
        expect(self.page.get_by_text("ACCOUNT DELETED!")).to_be_visible()
        self.page.locator('[data-qa="continue-button"]').click()
