# ca.indeed.com Job Postings Web Scraper
# Author: Eric Ng (github.com/eng69)
# Last updated: Sept. 6, 2020
"""
Web scraper for Indeed job postings within Vancouver with a default salary (if available) of $26k or higher.
Scrapes and retains duplicate postings.
Modified and updated from https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b.

Main program for web scraper.
"""

import pandas
import requests
import time
from bs4 import BeautifulSoup
from scraper import Scraper


def scrape_jobs():
    job_input = input("Enter your desired job position: ")
    # Format input job to insert into URL being scraped
    job = job_input.replace(" ", "+")

    # Job postings get more irrelevant after page 8, set max to 80
    max_results_per_city = 80
    cities = ["Vancouver", "Burnaby", "Richmond"]
    columns = ["city_searched", "job_title", "company_name", "location", "summary", "salary"]

    sample_dataframe = pandas.DataFrame(columns=columns)

    for city in cities:
        # To go to the next postings page, increment &start= by 10 in the URL
        for results in range(0, max_results_per_city, 10):
            URL = "https://ca.indeed.com/jobs?q=" + job + "+$26,000&l=" + city + ",+BC" + "&start=" + str(results)
            page = requests.get(URL)
            time.sleep(1)
            # lxml faster than html.parser default
            content = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
            row_num = len(sample_dataframe) + 1

            scraper = Scraper(content)

            # Get postings info from current page
            titles = scraper.extract_titles
            names = scraper.extract_company_names
            locations = scraper.extract_locations
            summaries = scraper.extract_summaries
            salaries = scraper.extract_salaries

            # Get corresponding postings info from info lists and add into dataframe
            for i in range(0, len(titles)):
                job_post = []
                job_post.extend([city, titles[i], names[i], locations[i], summaries[i], salaries[i]])
                # Update new dataframe row position to add posting
                new_row_num = row_num + i
                sample_dataframe.loc[new_row_num] = job_post
                print("Added job posting, row", new_row_num)

    # Convert dataframe to csv file
    filename = job + "_postings.csv"
    sample_dataframe.to_csv(filename, encoding="utf-8")
    print("\nFinished scraping. Postings saved to", filename)


if __name__ == "__main__":
    scrape_jobs()
