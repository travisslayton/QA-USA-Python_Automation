import time
import data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


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
        from_input = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_FROM))
        from_input.clear()
        from_input.send_keys(from_address)
        self.wait.until(lambda d: from_input.get_attribute('value') != "")
        actual_from = from_input.get_attribute('value')

        to_input = self.wait.until(EC.element_to_be_clickable(self.ADDRESS_TO))
        to_input.clear()
        to_input.send_keys(to_address)
        self.wait.until(lambda d: to_input.get_attribute('value') != "")
        actual_to = to_input.get_attribute('value')

        return actual_from, actual_to

    def call_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        plan_buttons = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "button.tcard-i")
        ))

        for button in plan_buttons:
            data_for = button.get_attribute("data-for")
            if data_for == "tariff-card-4":
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                self.driver.execute_script("arguments[0].click();", button)
                return True
        return False

    def reveal_phone_input_form(self):
        self.wait_for_overlay_to_disappear()
        reveal_form = self.wait.until(EC.element_to_be_clickable(self.REVEAL_PHONE_INPUT_FORM))
        reveal_form.click()

    def enter_phone_number(self, phone):
        self.wait_for_overlay_to_disappear()
        phone_input = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone)

    def wait_for_overlay_to_disappear(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.OVERLAY))
        except TimeoutException:
            pass

    def click_next_button(self):
        self.wait_for_overlay_to_disappear()
        next_btn = self.driver.find_element(*self.NEXT_BUTTON)
        next_btn.click()

    def enter_sms_code(self, code):
        sms_input = self.driver.find_element(*self.SMS_INPUT)
        sms_input.clear()
        sms_input.send_keys(code)

    def open_payment_method(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD)).click()

    def click_add_card(self):
        for attempt in range(5):
            try:
                add_card_btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON))
                add_card_btn.click()
                break
            except StaleElementReferenceException:
                time.sleep(1)

    def enter_card_number(self, number):
        card_input = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        card_input.clear()
        card_input.send_keys(number)

    def enter_card_code(self, code: str):
        code_input = self.wait.until(
            lambda driver: next(
                (el for el in driver.find_elements(*self.CARD_CODE_INPUT) if el.is_displayed()),
                None
            )
        )
        if code_input:
            code_input.clear()
            code_input.send_keys(code)
            self.driver.execute_script("arguments[0].blur();", code_input)

    def blur_card_code_field(self):
        self.driver.execute_script("arguments[0].blur();", self.driver.find_element(*self.CARD_CODE_INPUT))

    def wait_for_link_button_clickable(self, timeout=10):
        self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON))

    def click_link_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON)).click()

    def get_payment_method_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_METHOD_TEXT))
        return element.text.strip()

    def enter_driver_comment(self, comment_text):
        comment_field = self.wait.until(EC.visibility_of_element_located(self.COMMENT))
        comment_field.clear()
        comment_field.send_keys(comment_text)

    def get_driver_comment_text(self):
        comment_field = self.wait.until(EC.visibility_of_element_located(self.COMMENT))
        return comment_field.get_attribute("value") or comment_field.text

    def toggle_blanket_handkerchiefs(self):
        slider = self.wait.until(EC.element_to_be_clickable(self.BLANKET_HANDKERCHIEFS_SLIDER))
        slider.click()

    def is_blanket_handkerchiefs_added(self) -> bool:
        checkbox = self.driver.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')
        return checkbox.get_property("checked")

    def add_ice_cream(self, count=1):
        for _ in range(count):
            btn = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
            btn.click()

    def get_ice_cream_count(self):
        summary = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_SUMMARY))
        import re
        match = re.search(r'\d+', summary.text)
        return int(match.group()) if match else 0

    def is_car_search_modal_displayed(self, timeout=10):
        try:
            modal = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.CAR_SEARCH_MODAL)
            )
            return modal.is_displayed()
        except:
            return False
