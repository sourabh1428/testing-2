import csv
import os
from .base_page import BasePage

class LinkedInSearchPage(BasePage):
    def search_keyword(self, keyword):
        """
        Perform a LinkedIn search using the provided keyword.
        """
        search_url = f"https://www.linkedin.com/search/results/all/?keywords={keyword}&origin=TYPEAHEAD_HISTORY"
        self.page.goto(search_url)
        self.page.wait_for_selector("div.search-results-container")

    def scrape_user_profiles(self, max_posts=500, output_file="profiles.csv"):
        """
        Scrape user profiles for posts matching the search criteria, handle endless scrolling,
        and save extracted emails to a CSV file in real-time, printing each email found.

        :param max_posts: Maximum number of posts to collect.
        :param output_file: The name of the CSV file to save email profiles.
        :return: None
        """
        profiles = set()
        scroll_count = 0
        max_scroll_attempts = 100  # Max scroll attempts before stopping
        previous_height = None

        # Open the CSV file in append mode
        with open(output_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            file.seek(0, 2)  # Move to the end of the file to avoid overwriting
            if file.tell() == 0:  # Write header only if file is empty
                writer.writerow(["Email"])

            while len(profiles) < max_posts and scroll_count < max_scroll_attempts:
                # Extract user profile links (email addresses) in the current viewport
                self.page.wait_for_timeout(2000)  # Small delay to allow content to load
                current_profiles = self.page.locator("a[href^='mailto:']").evaluate_all(
                    "elements => elements.map(e => e.href.replace('mailto:', '').trim())"
                )

                # Add new profiles to the set
                new_profiles = set(current_profiles) - profiles
                profiles.update(new_profiles)

                # Write new profiles to the CSV file and print them
                for email in new_profiles:
                    writer.writerow([email])
                    file.flush()  # Ensure data is written immediately
                    os.fsync(file.fileno())  # Force data to be written to disk
                    print(f"Found email: {email}")  # Print each found email

                # Scroll down
                self.page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                self.page.wait_for_timeout(2000)  # Small delay after scrolling

                # Check if scrolling has reached the end
                current_height = self.page.evaluate("document.body.scrollHeight")
                if previous_height == current_height:  # No change in height
                    scroll_count += 1
                else:
                    scroll_count = 0  # Reset counter if new content is loaded

                previous_height = current_height

        print(f"Scraped profiles saved to {output_file} in real-time.")
