import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes server")


def test_set_route():
    # Add in S8
    print("function created for set route")
    pass


def test_select_plan():
    # Add in S8
    print("function created for select plan")
    pass


def test_fill_phone_number():
    # Add in S8
    print("function created for fill phone number")
    pass


def test_fill_card():
    # Add in S8
    print("function created for fill card")
    pass


def test_comment_for_driver():
    # Add in S8
    print("function created for comment for driver")
    pass


def test_order_blanket_and_handkerchiefs():
    # Add in S8
    print("function created for order blanket and handkerchiefs")
    pass


def test_order_2_ice_creams():
    for i in range(2):
        # Add in S8
        pass
    print("function created for order 2 ice creams")


def test_car_search_model_appears():
    # Add in S8
    print("function created for car search model appears")
    pass
