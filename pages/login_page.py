from .base_page import BasePage

class LinkedInLoginPage(BasePage):
    def load(self):
        self.page.goto("https://www.linkedin.com/login")

    def login(self, username, password):
        self.page.fill("input#username", username)
        self.page.fill("input#password", password)
        self.page.click("button[type='submit']")
        #self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector("input.search-global-typeahead__input")
