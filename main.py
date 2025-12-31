from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print('Connected to the Urban Routes server')
        else :
            print('Cannot connect to Urban Routes. Check the server is on and still running')

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert urban.get_from_address() == data.ADDRESS_FROM
        assert urban.get_to_address() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.select_plan()
        assert urban.get_selected_plan() == 'Supportive'

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.phone_number_field()
        urban.enter_phone_number(data.PHONE_NUMBER)
        urban.click_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        urban.enter_sms_code(code)
        urban.confirm_phone_number()
        assert urban.get_saved_phone() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.select_plan()
        urban.click_payment_method()
        urban.click_add_card()
        urban.enter_card_number(data.CARD_NUMBER)
        urban.enter_card_code(data.CARD_CODE)
        urban.click_link_button()
        urban.close_payment()
        assert urban.card_selected() == 'Card'

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.enter_driver_comment(data.MESSAGE_FOR_DRIVER)
        assert urban.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.select_plan()
        urban.blanket_switch()
        assert urban.check_switch()

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.select_plan()
        urban.add_ice_cream(2)
        assert urban.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        urban = UrbanRoutesPage(self.driver)
        urban.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        urban.select_plan()
        urban.enter_driver_comment(data.MESSAGE_FOR_DRIVER)
        urban.click_car_order_button()
        assert urban.get_car_order_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()