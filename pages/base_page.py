class BasePage:
    def __init__(self, page):
        self.page = page

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(2000)
