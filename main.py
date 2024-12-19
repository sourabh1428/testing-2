import os
from playwright.sync_api import sync_playwright
from scraper import LinkedInScraper
import csv
from datetime import datetime

def save_to_csv(data, keyword):
    """
    Save the extracted data to a CSV file.

    :param data: List of extracted emails.
    :param keyword: The keyword used for the search (to include in the filename).
    """
    # Generate a unique filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_keyword = keyword.replace(" ", "_").replace("@", "").replace("#", "")
    filename = f"extraction_{sanitized_keyword}_{timestamp}.csv"

    # Save data to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Email"])  # Header
        writer.writerows([[email] for email in data])  # Write each email as a row

    print(f"Emails saved to {filename}")


def main():
    keyword = "hiring software @"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        scraper = LinkedInScraper(browser)
        profiles = scraper.scrape(keyword)
        print(f"Found {len(profiles)} profiles for '{keyword}':")
        for i, profile in enumerate(profiles, 1):
            print(profile)
            # print(f"{i}: {profile}")
        save_to_csv(profiles,"data")
if __name__ == "__main__":
    main()
