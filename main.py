import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages import UrbanRoutesPage
import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium import webdriver
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        # Initialize Chrome driver
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        print("Browser launched and maximized")
        time.sleep(2)

        # Initialize page object
        cls.page = UrbanRoutesPage(cls.driver)
        print("UrbanRoutesPage initialized")

    def test_set_address(self):
        print("Starting test: set_address")
        self.driver.get(data.URBAN_ROUTES_URL)
        print("Navigated to Urban Routes URL")
        ADDRESS_FROM, ADDRESS_TO = self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print(f"Set addresses: From='{ADDRESS_FROM}', To='{ADDRESS_TO}'")
        assert "East 2nd Street, 601" in ADDRESS_FROM
        assert "1300 1st St" in ADDRESS_TO
        print("Addresses verified successfully\n")

    def test_select_supportive_plan(self):
        print("Starting test: select_supportive_plan")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")

        # Verify supportive plan selected by checking for "active" class on the tariff-card-4 button
        supportive_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
        assert "active" in supportive_button.get_attribute("class"), "Supportive Plan button not active"
        print("Assertion passed: Supportive Plan is active\n")

    def test_enter_phone_number(self):
        print("Starting test: enter_phone_number")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")
        self.page.reveal_phone_input_form()
        print("Phone input form revealed")
        self.page.enter_phone_number(data.PHONE_NUMBER)
        print(f"Entered phone number: {data.PHONE_NUMBER}")
        self.page.click_next_button()
        print("Clicked Next button")

        code = None
        for i in range(20):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    print(f"SMS code retrieved: {code}")
                    break
            except Exception:
                print(f"Retry {i + 1}/20 for SMS code...")
                time.sleep(2)
        assert code, "Phone confirmation code not retrieved"
        self.page.enter_sms_code(code)
        print("SMS code entered successfully\n")

    def test_add_credit_card(self):
        print("Starting test: add_credit_card")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")
        self.page.open_payment_method()
        print("Payment method opened")
        self.page.click_add_card()
        print("'Add Card' button clicked")
        self.page.enter_card_number(data.CARD_NUMBER)
        print(f"Entered card number: {data.CARD_NUMBER}")
        self.page.enter_card_code(data.CARD_CODE)
        print(f"Entered card code: {data.CARD_CODE}")
        self.page.blur_card_code_field()
        print("Blurred card code field")
        self.page.wait_for_link_button_clickable()
        print("'Link' button is clickable")
        self.page.click_link_button()
        print("'Link' button clicked")
        payment_text = self.page.get_payment_method_text()
        assert payment_text == "Card"
        print("Credit card added and verified successfully\n")

    def test_comment_for_driver(self):
        print("Starting test: comment_for_driver")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")
        self.page.enter_driver_comment(data.COMMENT)
        print(f"Entered driver comment: {data.COMMENT}")
        stored_comment = self.page.get_driver_comment_text()
        assert stored_comment == data.COMMENT
        print("Driver comment verified successfully\n")

    def test_order_blanket_and_handkerchiefs(self):
        print("Starting test: order_blanket_and_handkerchiefs")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")
        self.page.toggle_blanket_handkerchiefs()
        print("Toggled Blanket and Handkerchiefs")
        assert self.page.is_blanket_handkerchiefs_added()
        print("Blanket and Handkerchiefs verified successfully\n")

    def test_order_2_ice_creams(self):
        print("Starting test: order_2_ice_creams")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")
        self.page.add_ice_cream(count=2)
        print("Added 2 ice creams")
        ice_cream_count = self.page.get_ice_cream_count()
        assert ice_cream_count == 2
        print("Ice cream count verified successfully\n")

    def test_car_search_modal_appears(self):
        print("Starting test: car_search_modal_appears")
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked")
        self.page.select_supportive_plan()
        print("Supportive Plan selected")
        self.page.reveal_phone_input_form()
        print("Phone input form revealed")
        self.page.enter_phone_number(data.PHONE_NUMBER)
        print(f"Entered phone number: {data.PHONE_NUMBER}")
        self.page.click_next_button()
        print("Clicked Next button")

        code = None
        for i in range(20):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    print(f"SMS code retrieved: {code}")
                    break
            except Exception:
                print(f"Retry {i + 1}/20 for SMS code...")
                time.sleep(2)
        assert code, "SMS code not retrieved"
        self.page.enter_sms_code(code)
        print("SMS code entered")

        wait = WebDriverWait(self.driver, 15)
        confirm_btn = wait.until(EC.element_to_be_clickable(self.page.CONFIRM_BUTTON))
        confirm_btn.click()
        print("Clicked Confirm button")

        self.page.enter_driver_comment(data.COMMENT)
        print(f"Entered driver comment: {data.COMMENT}")

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.page.ORDER_BUTTON)
        ).click()
        print("Clicked Order button")

        wait = WebDriverWait(self.driver, 40)
        modal = wait.until(EC.visibility_of_element_located(self.page.CAR_SEARCH_MODAL))
        assert modal.is_displayed()
        print("Car search modal verified successfully\n")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
        print("Browser closed")
