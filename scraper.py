# ca.indeed.com Job Postings Web Scraper
# Author: Eric Ng (github.com/eng69)
# Last updated: Sept. 6, 2020
"""
Web scraper for Indeed job postings within Vancouver with a default salary (if available) of $26k or higher.
Scrapes and retains duplicate postings.
Modified and updated from https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b.

Job posting web scraper.
"""


class Scraper:
    """Scraper class"""
    def __init__(self, content):
        """Instantiates a Scraper object"""
        self._content = content

    @property
    def extract_titles(self):
        """Extracts job titles from postings page"""
        titles = []
        for div in self._content.find_all(name="div", attrs={"class": "row"}):
            for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                titles.append(a.text.strip())

        return titles

    @property
    def extract_company_names(self):
        """Extracts company names from postings page"""
        names = []
        for div in self._content.find_all(name="div", attrs={"class": "row"}):
            for span in div.find_all(name="span", attrs={"class": "company"}):
                names.append(span.text.strip())

        return names

    @property
    def extract_locations(self):
        """Extracts job locations from postings page"""
        locations = []
        for div in self._content.find_all(attrs={"class": "location"}):
            locations.append(div.text.strip())

        return locations

    @property
    def extract_salaries(self):
        """Extracts job salaries from postings page"""
        salaries = []
        # Try to find posted salary. If there is none, append "no salary listed" to the list instead
        for div in self._content.find_all(name="div", attrs={"class": "row"}):
            try:
                salaries.append(div.find(name="span", attrs={"class": "salaryText"}).text.strip())
            except:
                salaries.append("No_salary_listed")

        return salaries

    @property
    def extract_summaries(self):
        """Extracts job summaries from postings page"""
        summaries = []
        for div in self._content.find_all(name="div", attrs={"class": "summary"}):
            # Each summary posting might be split into different list items, combine them first
            summary = ""
            for li in div.find_all(name="li"):
                summary += f"{li.text.strip()} "
            summaries.append(summary)

        return summaries
