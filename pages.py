from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import data
import helpers

class UrbanRoutesPage:
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_A_TAXI_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Call a taxi"]')

    SUPPORTIVE_PLAN_LOCATOR = (By.XPATH, '(//div[text()="Supportive"])[1]')
    SUPPORTIVE_PLAN_ACTIVE = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title" and text()="Supportive"]')

    CARD_NUMBER_LOCATOR = (By.XPATH, '//input[@id="cardNumber"]')
    NEXT_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Next"]')
    SMS_CODE_LOCATOR = (By.CSS_SELECTOR, '#code.input')
    CARD_LOCATOR = (By.XPATH, '//input[@id="cardCode"]')
    PHONE_NUMBER_LOCATOR = (By.CLASS_NAME, 'np-text')
    PHONE_NUMBER_CONFIRM_LOCATOR = (By.XPATH, '//button[contains(text(), "Confirm")]')

    PHONE_NUMBER_INPUT_LOCATOR = (By.ID, 'phone')
    CODE_LOCATOR = (By.CSS_SELECTOR, '#code.card-input')
    PAYMENT_METHOD_LOCATOR = (By.CSS_SELECTOR, '.pp-button.filled')
    ADD_CARD_LOCATOR = (By.CSS_SELECTOR, '.pp-plus-container')
    ENTER_CARD_NUMBER_LOCATOR = (By.CSS_SELECTOR, '#number.card-input')
    LINK_LOCATOR = (By.XPATH, "//button[@class='button full' and text()='Link']")
    CARD_CONFIRM_LOCATOR = (By.XPATH, '//button[text()="Confirm"]')
    CLOSE_PAYMENT_METHOD_LOCATOR = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    CARD_PAYMENT_SELECTED_LOCATOR = (By.CLASS_NAME, 'pp-value-text')

    COMMENT_BUTTON_LOCATOR = (By.ID, 'comment')

    BLANKET_SWITCH_LOCATOR = (By.CSS_SELECTOR, '.switch')
    CHECK_SWITCH_LOCATOR = (By.CSS_SELECTOR, '.switch-input')

    ICE_CREAM_LOCATOR = (By.CSS_SELECTOR, '.counter-plus')
    ICE_CREAM_COUNT_LOCATOR = (By.CSS_SELECTOR, '.counter-value')

    CAR_ORDER_BUTTON_LOCATOR = (By.CSS_SELECTOR, '.smart-button')
    CAR_SEARCH_WINDOW_LOCATOR = (By.CSS_SELECTOR, '.order-header-title')


    def __init__(self, driver):
        self.driver = driver

    def enter_from_location(self, from_text):
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_text)

    def enter_to_location(self, to_text):
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_text)

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_attribute('value')

    def get_to_address(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_attribute('value')

    def click_call_taxi_button(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.CALL_A_TAXI_BUTTON_LOCATOR)).click()

    def set_route(self, from_address, to_address):
        self.enter_from_location(from_address)
        self.enter_to_location(to_address)
        self.click_call_taxi_button()

    def select_plan(self):
        self.driver.find_element(*self.SUPPORTIVE_PLAN_LOCATOR).click()

    def get_selected_plan(self):
        return self.driver.find_element(*self.SUPPORTIVE_PLAN_ACTIVE).text

    def phone_number_field(self):
        self.driver.find_element(*self.PHONE_NUMBER_LOCATOR).click()

    def enter_phone_number(self, phone_number):
        self.driver.find_element(*self.PHONE_NUMBER_INPUT_LOCATOR).send_keys(phone_number)

    def enter_sms_code(self, code):
        self.driver.find_element(*self.SMS_CODE_LOCATOR).send_keys(code)

    def get_saved_phone(self):
        return self.driver.find_element(*self.PHONE_NUMBER_LOCATOR).text

    def confirm_phone_number(self):
        self.driver.find_element(*self.PHONE_NUMBER_CONFIRM_LOCATOR).click()

    def close_payment(self):
        self.driver.find_element(*self.CLOSE_PAYMENT_METHOD_LOCATOR).click()

    def card_selected(self):
        return self.driver.find_element(*self.CARD_PAYMENT_SELECTED_LOCATOR).text

    def click_payment_method(self):
        wait = WebDriverWait(self.driver, 15)
        payment_method = wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_LOCATOR)
        )
        payment_method.click()

    def click_link_button(self):
        self.driver.find_element(*self.LINK_LOCATOR).click()

    def click_add_card(self):
        wait = WebDriverWait(self.driver, 15)

        wait.until(EC.visibility_of_element_located(self.ADD_CARD_LOCATOR))
        add_card = wait.until(EC.element_to_be_clickable(self.ADD_CARD_LOCATOR))

        add_card.click()

    def enter_card_number(self, number):
        self.driver.find_element(*self.ENTER_CARD_NUMBER_LOCATOR).send_keys(number)

    def click_next_button(self):
        self.driver.find_element(*self.NEXT_BUTTON_LOCATOR).click()

    def enter_card_code(self, code):
        self.driver.find_element(*self.CODE_LOCATOR).send_keys(code)
        self.driver.find_element(*self.CODE_LOCATOR).send_keys(Keys.TAB)

    def click_supportive_plan(self):
        self.driver.find_element(*self.SUPPORTIVE_PLAN_LOCATOR).click()

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_BUTTON_LOCATOR).get_attribute('value')

    def enter_driver_comment(self, comment_text):
        self.driver.find_element(*self.COMMENT_BUTTON_LOCATOR).send_keys(comment_text)

    def blanket_switch(self):
        self.driver.find_element(*self.BLANKET_SWITCH_LOCATOR).click()

    def check_switch(self):
        return self.driver.find_element(*self.CHECK_SWITCH_LOCATOR).get_property('checked')

    def add_ice_cream(self, amount: int):
        option_add_controls = self.driver.find_elements(*self.ICE_CREAM_LOCATOR)
        for count in range(amount):
            option_add_controls[0].click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT_LOCATOR).text)

    def click_car_order_button(self):
        self.driver.find_element(*self.CAR_ORDER_BUTTON_LOCATOR).click()

    def get_car_order_visible(self):
        return self.driver.find_element(*self.CAR_SEARCH_WINDOW_LOCATOR).is_displayed()