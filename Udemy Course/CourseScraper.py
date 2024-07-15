import time
import pandas as pd
from datetime import datetime
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
from halo import Halo
from tqdm import tqdm

class CourseScraper:
    def __init__(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        self.driver = None
        self.base_url = "https://www.onlinecourses.ooo/"
        self.course_details = []
        self.search_keyword = ""
        self.num_pages = 0
        self.options = firefox_options
    
    def get_driver(self):
        self.driver = webdriver.Firefox(options=self.options)
    
    def get_course_links(self, soup):
        records = soup.find_all('div', class_='news-community clearfix')
        links = set()

        for record in records:
            title_tag = record.find('h2', class_='font130 mt0 mb10 mobfont120 lineheight25')
            link_tag = title_tag.find('a') if title_tag else None
            link = link_tag['href'] if link_tag else "No link"
            links.add(link)

        return links

    def extract_course_details(self, link):
        self.driver.get(link)
        spinner = Halo(text="Loading course details...", spinner='dots')
        spinner.start()

        time.sleep(3)

        new_html = self.driver.page_source
        new_soup = BeautifulSoup(new_html, 'lxml')

        course_title_tag = new_soup.find('h1')
        course_title = course_title_tag.get_text(strip=True) if course_title_tag else "No course title"

        redeem_coupon_tag = new_soup.find('a', class_='btn_offer_block re_track_btn')
        redeem_coupon_url = redeem_coupon_tag['href'] if redeem_coupon_tag else None

        if redeem_coupon_url:
            parsed_url = urllib.parse.urlparse(redeem_coupon_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            redeem_coupon_code = query_params.get('couponCode', ['No coupon Needed'])[0]
        else:
            redeem_coupon_code = "No coupon Needed"

        self.course_details.append({
            'Course Title': course_title,
            'Course Link': redeem_coupon_url,
            'Redeem Coupon Code': redeem_coupon_code
        })

        spinner.succeed("Course details loaded.")  

    def get_num_pages(self, soup):
        pagination = soup.find('ul', class_='page-numbers')
        if pagination:
            pages = pagination.find_all('li')
            page_numbers = [int(page.get_text()) for page in pages if page.get_text().isdigit()]
            return max(page_numbers)
        else:
            return 1

    def scrape_courses(self, keyword, num_pages):
        self.driver.get(self.base_url)
        time.sleep(2)

        search = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="s"]')))
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)

        time.sleep(3)

        self.search_keyword = keyword

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        self.num_pages = self.get_num_pages(soup)

        current_page = 1
        while current_page <= min(num_pages, self.num_pages):
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            links_to_open = self.get_course_links(soup)
            
            print(f"Scraping courses from page {current_page} of {min(num_pages, self.num_pages)}...")
            
            for link in tqdm(links_to_open, desc="Extracting course details"):
                self.extract_course_details(link)
            
            if current_page < min(num_pages, self.num_pages):
                next_button = soup.find('li', class_='next_paginate_link')
                if next_button:
                    next_link = next_button.find('a')['href']
                    self.driver.get(next_link)
                    time.sleep(3)
                    current_page += 1
                else:
                    break  
            else:
                break

    def export_to_excel(self):
        print("Exporting course details to Excel...")
        df = pd.DataFrame(self.course_details)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"course_details_{self.search_keyword}_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        print(f"Course details exported to {filename}")

    def run(self):
        try:
            keyword = input("Enter the keyword to search for courses: ")
            print("Loading page count...")
            self.get_driver()
            self.scrape_courses(keyword, self.num_pages)
            print("\033[F\033[K", end="")
            print(f"Total pages found: {self.num_pages}")
            num_pages_to_scrape = int(input(f"How many pages out of {self.num_pages} do you want to scrape?: "))
            
            self.scrape_courses(keyword, num_pages_to_scrape)
            self.export_to_excel()
        except ValueError:
            print("Invalid input. Please enter a valid number of pages.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = CourseScraper()
    scraper.run()

