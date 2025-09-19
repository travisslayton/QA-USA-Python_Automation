import time
import data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get(data.URBAN_ROUTES_URL)

    # Locators
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(), 'Call a taxi')]")
    SUPPORTIVE_PLAN = (By.CSS_SELECTOR, "button[data-for='tariff-card-4']")
    PHONE_INPUT = (By.XPATH, '//*[@id="phone"]')
    PHONE_MODAL = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[2]/div')
    SMS_INPUT = (By.XPATH, "//*[@id='code']")
    CONFIRM_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    REVEAL_PHONE_INPUT_FORM = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    OVERLAY = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]')
    NEXT_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    PAYMENT_METHOD = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    ADD_CARD_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    CARD_NUMBER_INPUT = (By.XPATH, '//*[@id="number"]')
    CARD_CODE_INPUT = (By.XPATH, '//*[@id="code"]')
    LINK_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    PAYMENT_METHOD_TEXT = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]')
    COMMENT = (By.XPATH, '//*[@id="comment"]')
    COMMENT_TEXT = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div')
    BLANKET_HANDKERCHIEFS_SLIDER = (By.XPATH,
                                    '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    ICE_CREAM_PLUS_BUTTON = (By.XPATH,
                             '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    ICE_CREAM_SUMMARY = (By.XPATH,
                         '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div')
    ORDER_BUTTON = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
    CAR_SEARCH_MODAL = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[2]/div')

    def set_address(self, from_address, to_address):
        wait = WebDriverWait(self.driver, 10)

        # Handle "From" field
        from_input = wait.until(EC.element_to_be_clickable(self.ADDRESS_FROM))
        from_input.clear()
        from_input.send_keys(from_address)

        # Wait until value is not empty
        wait.until(lambda d: from_input.get_attribute('value') != "")

        # Check with containment instead of strict equality
        actual_from = from_input.get_attribute('value')
        assert from_address in actual_from, f"Expected '{from_address}' to be part of '{actual_from}'"

        # Handle "To" field
        to_input = wait.until(EC.element_to_be_clickable(self.ADDRESS_TO))
        to_input.clear()
        to_input.send_keys(to_address)

        # Same for "To"
        wait.until(lambda d: to_input.get_attribute('value') != "")
        actual_to = to_input.get_attribute('value')
        assert to_address in actual_to, f"Expected '{to_address}' to be part of '{actual_to}'"

    def call_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        print("Waiting for plan options to load...")

        # Wait for all plan buttons to appear
        plan_buttons = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button.tcard-i")
        ))

        print(f"Found {len(plan_buttons)} plan buttons.")

        # Find the one with 'tariff-card-4' or the "active" class, depending on your HTML
        for button in plan_buttons:
            data_for = button.get_attribute("data-for")
            class_attr = button.get_attribute("class")
            is_displayed = button.is_displayed()
            print(f"Checking button - data-for: {data_for}, class: {class_attr}, displayed: {is_displayed}")

            if data_for == "tariff-card-4":
                print("Scrolling into view and clicking Supportive Plan button...")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                self.driver.execute_script("arguments[0].click();", button)
                print("Supportive Plan selected.")
                return

        raise Exception("Supportive Plan button (data-for='tariff-card-4') not found.")

    def reveal_phone_input_form(self):
        print("Waiting for overlay to disappear before clicking phone input reveal...")
        self.wait_for_overlay_to_disappear()
        reveal_form = self.wait.until(EC.element_to_be_clickable(self.REVEAL_PHONE_INPUT_FORM))
        reveal_form.click()
        print("Clicked to reveal phone input.")

    def enter_phone_number(self, phone):
        print("Waiting for overlay to disappear before typing phone number...")
        self.wait_for_overlay_to_disappear()
        phone_input = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone)
        print(f"Entered phone number: {phone}")

    def wait_for_overlay_to_disappear(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.OVERLAY))
            print("Overlay disappeared.")
        except TimeoutException:
            print("Overlay did not disappear, continuing anyway...")

    def click_next_button(self):
        try:
            # Wait for overlay to disappear first
            self.wait_for_overlay_to_disappear()
            next_btn = self.driver.find_element(*self.NEXT_BUTTON)
            next_btn.click()
            print("Clicked Next button")
        except TimeoutException:
            print("Overlay still present, using JS click for Next button")
            self.js_click_next_button()  # fallback if overlay persists

    def enter_sms_code(self, code):
        sms_input = self.driver.find_element(*self.SMS_INPUT)
        sms_input.clear()
        sms_input.send_keys(code)
        print(f"Entered SMS code: {code}")

    def open_payment_method(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD)).click()
        print("Payment method opened")

    def click_add_card(self):
        for attempt in range(5):  # retry up to 5 times
            try:
                add_card_btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON))
                add_card_btn.click()
                print("Add Card button clicked successfully.")
                break
            except StaleElementReferenceException:
                print(f"Stale element encountered, retrying click... ({attempt + 1}/5)")
                time.sleep(1)
        else:
            raise Exception("Failed to click Add Card button after multiple attempts.")

    def enter_card_number(self, number):
        card_input = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        card_input.clear()
        card_input.send_keys(number)
        print(f"Entered card number: {number}")

    def enter_card_code(self, code: str):
        """
        Enter the card security code (CVV) safely.
        Since the SMS input and card code input share the same XPath,
        we target only the visible input after revealing the card form.
        """
        # Wait until a visible input appears
        code_input = self.wait.until(
            lambda driver: next(
                (el for el in driver.find_elements(*self.CARD_CODE_INPUT) if el.is_displayed()),
                None
            )
        )

        if not code_input:
            raise Exception("No visible card code input found")

        # Enter the code
        code_input.clear()
        code_input.send_keys(code)

        # Optionally, blur the field to trigger validation (TAB or click outside)
        self.driver.execute_script("arguments[0].blur();", code_input)
        print(f"Entered card code: {code}")

    def blur_card_code_field(self):
        # Either click outside the field or send TAB key to trigger validation
        self.driver.execute_script("arguments[0].blur();", self.driver.find_element(*self.CARD_CODE_INPUT))
        print("Blurred card code field to trigger validation")

    def wait_for_link_button_clickable(self, timeout=10):
        self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON))
        print("Link button is now clickable")

    def click_link_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON)).click()
        print("Clicked Link button to add card")

    def get_payment_method_text(self):
        payment_text_locator = self.PAYMENT_METHOD_TEXT  # your updated XPath
        element = self.wait.until(EC.visibility_of_element_located(payment_text_locator))
        text = element.text.strip()
        if "Card" in text:
            return "Card"
        return text  # for debug/logging purposes

    def enter_driver_comment(self, comment_text):
        comment_field = self.wait.until(EC.visibility_of_element_located(self.COMMENT))
        comment_field.clear()
        comment_field.send_keys(comment_text)
        print(f"Entered driver comment: {comment_text}")

    # Method to retrieve comment text
    def get_driver_comment_text(self):
        comment_field = self.wait.until(EC.visibility_of_element_located(self.COMMENT))
        # Use text property if value is None
        return comment_field.get_attribute("value") or comment_field.text

    def toggle_blanket_handkerchiefs(self):
        slider = self.wait.until(EC.element_to_be_clickable(self.BLANKET_HANDKERCHIEFS_SLIDER))
        slider.click()
        print("Clicked Blanket and Handkerchiefs slider")

    # Page method to verify selection
    def is_blanket_handkerchiefs_added(self) -> bool:
        checkbox = self.driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')
        checked = checkbox.get_property("checked")
        print(f"Blanket and Handkerchiefs checkbox checked: {checked}")
        return checked

    # Method to add ice cream
    def add_ice_cream(self, count=1):
        for _ in range(count):
            btn = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
            btn.click()
            print("Clicked Ice Cream plus button")

    # Method to get current ice cream count from summary
    def get_ice_cream_count(self):
        summary = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_SUMMARY))
        # Assuming the count is displayed as text inside the container
        text = summary.text
        # Extract digits from the text
        import re
        match = re.search(r'\d+', text)
        return int(match.group()) if match else 0

    def place_order(self, sms_code="1234", timeout=30):
        wait = WebDriverWait(self.driver, timeout)

        # Step 1: Click Next after entering phone
        try:
            next_btn = wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
            next_btn.click()
        except Exception as e:
            print("Failed to click Next after phone input:", e)
            return

        # Step 2: Wait for SMS input, enter code, and click Confirm
        try:
            sms_input = wait.until(EC.visibility_of_element_located(self.SMS_INPUT))
            sms_input.clear()
            sms_input.send_keys(sms_code)

            confirm_btn = wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON))
            confirm_btn.click()
        except Exception as e:
            print("Failed to enter SMS code or click Confirm:", e)
            return

        # Step 3: Wait for overlay (if any) to disappear
        try:
            wait.until(EC.invisibility_of_element_located(self.OVERLAY))
        except Exception:
            print("Overlay did not disappear, continuing anyway...")

        # Step 4: Click the order button
        try:
            order_btn = wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON))
            order_btn.click()
        except Exception as e:
            print("Failed to click Order button:", e)

    def is_car_search_modal_displayed(self, timeout=10):
        """Wait for and check if the car search modal is visible"""
        try:
            modal = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.CAR_SEARCH_MODAL)
            )
            return modal.is_displayed()
        except:
            return False
