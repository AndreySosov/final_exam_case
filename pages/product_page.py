import math
from selenium.common.exceptions import NoAlertPresentException
from .base_page import BasePage
from .locators import ProductPageLocators

class ProductPage(BasePage):
    product_name = ''
    product_price = ''
    product_decription = ''

    def add_product_to_basket(self):
        self.should_be_name()
        self.should_be_price()
        self.should_be_decription()
        self.should_be_add_button()

        btn = self.browser.find_element(*ProductPageLocators.BTN_ADD_TO_BASKET)
        btn.click()
        self.solve_quiz_and_get_code()

        self.should_be_success()
        self.check_success_message()

    def should_be_name(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_NAME), "Name of product not found"
        self.product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def should_be_price(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_PRICE), "Price of product not found"
        self.product_price = self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def should_be_decription(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_DESCRIPTION), "Description of product not found"
        self.product_decription = self.browser.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION).text

    def should_be_success(self):
        assert self.is_element_present(*ProductPageLocators.SUCCESS_MESSAGES), "Message of Success added product in " \
                                                                               "basket not found "

    def should_be_add_button(self):
        assert self.is_element_present(*ProductPageLocators.BTN_ADD_TO_BASKET), "Button 'Add to basket' is not " \
                                                                                "presented "

    def check_success_message(self):
        msg_lst = self.browser.find_elements(*ProductPageLocators.SUCCESS_MESSAGES)
        assert len(msg_lst) == 3, "Success message not found"

        assert self.product_name == msg_lst[0].text, "Wrong name product added to basket"
        assert self.product_price == msg_lst[2].text, "Wrong price product added to basket"

    def solve_quiz_and_get_code(self):
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")