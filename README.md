**CourseScraper**
CourseScraper is a Python-based web scraper that extracts course details from the website Online Courses. It uses Selenium to automate browser actions and BeautifulSoup to parse HTML content. The scraped course details are exported to an Excel file.

**Features**
Automated Web Scraping: Uses Selenium WebDriver to automate the scraping process.
Course Details Extraction: Extracts course titles, links, and redeem coupon codes.
Pagination Handling: Scrapes multiple pages of search results.
Excel Export: Exports the scraped data to an Excel file.
**Requirements**
Python 3.6+
pandas
selenium
beautifulsoup4
lxml
halo
tqdm


**Installation**
**Clone the Repository:**
git clone https://github.com/yourusername/CourseScraper.git
cd CourseScraper
Install Dependencies:

Install the required Python packages using pip:
pip install pandas selenium beautifulsoup4 lxml halo tqdm
GeckoDriver:

Ensure you have the GeckoDriver installed for Firefox. You can download it from GeckoDriver releases and add it to your system PATH.

**Usage**
Run the Scraper:
python scraper.py
Input Search Keyword:
When prompted, enter the keyword to search for courses.

**Specify Number of Pages to Scrape:**
The scraper will first determine the total number of pages available for the search keyword. You will then be prompted to enter the number of pages you want to scrape.

**Excel Export:**
The scraped course details will be exported to an Excel file with a timestamped filename.

**Code Overview**
**CourseScraper Class:**
__init__(): Initializes the scraper with necessary options.
**get_driver()**: Initializes the Selenium WebDriver.
**get_course_links():** Extracts course links from a given BeautifulSoup object.
**extract_course_details():** Extracts course details from a given link.
**get_num_pages():** Determines the total number of pages for a given search keyword.
**scrape_courses():** Manages the scraping process, including pagination.
**export_to_excel():** Exports the scraped data to an Excel file.
**run():** Main method to run the scraper, handles user input and error management.
