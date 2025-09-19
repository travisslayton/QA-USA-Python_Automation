import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import UrbanRoutesPage
from selenium.webdriver.common.by import By
import data
import helpers
import time


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Import Selenium classes
        from selenium import webdriver
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        # Initialize Chrome driver
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        time.sleep(2)

    def test_set_address(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")
        time.sleep(2)

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")
        time.sleep(2)

    def test_enter_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")

        print("Step 4: Revealing phone input form...")
        self.page.reveal_phone_input_form()
        print("Phone input form revealed.")

        print(f"Step 5: Entering phone number: {data.PHONE_NUMBER}...")
        self.page.enter_phone_number(data.PHONE_NUMBER)
        self.page.click_next_button()
        print("Phone number entered and Next button clicked.")

        print("Step 6: Polling for SMS confirmation code...")
        code = None
        for i in range(20):
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    print(f"SMS code retrieved: {code}")
                    break
            except Exception:
                print(f"SMS code not found yet, retry {i + 1}/20...")
                time.sleep(2)
        if not code:
            raise Exception("Phone confirmation code still not found after waiting.")

        print(f"Step 7: Entering SMS code: {code}...")
        self.page.enter_sms_code(code)
        print("SMS code entered.")

    def test_add_credit_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")

        print("Step 4: Opening Payment Method...")
        self.page.open_payment_method()
        print("Payment method opened.")

        print("Step 5: Clicking 'Add Card'...")
        self.page.click_add_card()
        print("'Add Card' clicked.")

        print(f"Step 6: Entering card number: {data.CARD_NUMBER} and code: {data.CARD_CODE}...")
        self.page.enter_card_number(data.CARD_NUMBER)
        self.page.enter_card_code(data.CARD_CODE)

        print("Step 7: Changing focus to trigger validation...")
        self.page.blur_card_code_field()

        print("Step 8: Waiting for 'Link' button to become clickable...")
        self.page.wait_for_link_button_clickable()

        print("Step 9: Clicking 'Link' to add card...")
        self.page.click_link_button()
        print("'Link' clicked.")

        print("Step 10: Verifying that card was added successfully...")
        payment_text = self.page.get_payment_method_text()
        print(f"Payment method text: {payment_text}")
        time.sleep(2)
        assert payment_text == "Card", f"Expected payment method to be 'Card', got '{payment_text}'"
        print("Credit card added successfully.")

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")

        print(f"Step 4: Entering driver comment: {data.COMMENT}...")
        self.page.enter_driver_comment(data.COMMENT)
        print("Driver comment entered.")

        print("Step 5: Verifying stored driver comment...")
        stored_comment = self.page.get_driver_comment_text()
        print(f"Stored comment: {stored_comment}")
        time.sleep(2)
        assert stored_comment == data.COMMENT, f"Expected comment '{data.COMMENT}', got '{stored_comment}'"
        print("Driver comment verified successfully.")

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")

        print("Step 4: Toggling Blanket and Handkerchiefs...")
        self.page.toggle_blanket_handkerchiefs()
        print("Blanket and Handkerchiefs toggled.")

        print("Step 5: Verifying Blanket and Handkerchiefs selection...")
        added = self.page.is_blanket_handkerchiefs_added()
        print(f"Selection confirmed: {added}")
        time.sleep(2)
        assert added, "Blanket and Handkerchiefs selection was not confirmed"
        print("Blanket and Handkerchiefs selection verified successfully.")

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")

        print("Step 4: Adding 2 Ice Creams...")
        self.page.add_ice_cream(count=2)
        print("Ice Creams added.")

        print("Step 5: Verifying Ice Cream count...")
        ice_cream_count = self.page.get_ice_cream_count()
        print(f"Ice Cream count: {ice_cream_count}")
        time.sleep(2)
        assert ice_cream_count == 2, f"Expected 2 ice creams, got {ice_cream_count}"
        print("Ice Cream count verified successfully.")

    def test_car_search_modal_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

        # Step 1: Set addresses
        print("Step 1: Setting addresses...")
        self.page.set_address("East 2nd Street, 601", "1300 1st St")
        print("Addresses set successfully.")

        # Step 2: Call a Taxi
        print("Step 2: Clicking 'Call a Taxi' button...")
        self.page.call_taxi_button()
        print("'Call a Taxi' button clicked.")

        # Step 3: Select the Supportive Plan
        print("Step 3: Selecting the Supportive Plan...")
        self.page.select_supportive_plan()
        print("Supportive Plan selected.")

        # Step 4: Reveal phone input form and enter phone number
        print("Step 4: Revealing phone input form...")
        self.page.reveal_phone_input_form()
        print("Phone input form revealed.")
        print(f"Entering phone number: {data.PHONE_NUMBER}...")
        self.page.enter_phone_number(data.PHONE_NUMBER)
        self.page.click_next_button()
        print("Phone number entered and Next button clicked.")

        # Step 5: Poll for SMS code
        print("Step 5: Polling for SMS confirmation code...")
        code = None
        for i in range(20):  # wait up to ~40s
            try:
                code = helpers.retrieve_phone_code(self.driver)
                if code:
                    print(f"SMS code retrieved: {code}")
                    break
            except Exception:
                print(f"SMS code not found yet, retry {i + 1}/20...")
                time.sleep(2)
        if not code:
            raise Exception("Phone confirmation code not found after waiting.")

        # Step 6: Enter SMS code
        print(f"Step 6: Entering SMS code: {code}...")
        self.page.enter_sms_code(code)
        print("SMS code entered.")

        # Step 7: Click Confirm button after entering SMS code
        print("Step 7: Clicking Confirm button...")
        wait = WebDriverWait(self.driver, 15)
        confirm_btn = wait.until(EC.element_to_be_clickable(self.page.CONFIRM_BUTTON))
        confirm_btn.click()
        print("Confirm button clicked.")

        # Step 8: Enter a message for the driver
        print(f"Step 8: Entering driver comment: {data.COMMENT}...")
        self.page.enter_driver_comment(data.COMMENT)
        print("Driver comment entered.")

        # Step 9: Click the Order button
        print("Step 9: Clicking Order button...")
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.page.ORDER_BUTTON)
        ).click()
        print("Order button clicked.")

        # Step 10: Verify the car search modal appears
        print("Step 10: Verifying that the car search modal appears...")
        print("CAR_SEARCH_MODAL locator:", self.page.CAR_SEARCH_MODAL)

        time.sleep(2)  # buffer for animations

        wait = WebDriverWait(self.driver, 40)  # increased timeout
        modal = wait.until(EC.visibility_of_element_located(self.page.CAR_SEARCH_MODAL))
        assert modal.is_displayed(), "Car search modal did not appear after placing order"
        print("Car search modal is displayed successfully.")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
