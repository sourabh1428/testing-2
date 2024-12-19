from config.credentials import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
from config.settings import CONTEXT_FILE, MAX_POSTS
from utils.context_manager import save_context, load_context
from pages.login_page import LinkedInLoginPage
from pages.search_page import LinkedInSearchPage
import os

class LinkedInScraper:
    def __init__(self, browser, context_path=CONTEXT_FILE):
        self.browser = browser
        self.context_path = context_path

    def scrape(self, keyword):
        # Check if the context file exists
        if os.path.exists(self.context_path):
            print(f"Loading saved context from {self.context_path}")
            context = load_context(self.browser, self.context_path)
        else:
            print("No saved context found. Logging in...")
            context = self.browser.new_context()
            page = context.new_page()
            login_page = LinkedInLoginPage(page)
            login_page.load()
            login_page.login(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
            #breakpoint()
            save_context(page, self.context_path)

        # Open a new page in the existing context and scrape
        page = context.new_page()
        search_page = LinkedInSearchPage(page)
        search_page.search_keyword(keyword)
        profiles = search_page.scrape_user_profiles(MAX_POSTS)

        return profiles
