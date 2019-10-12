from selenium import webdriver
from bs4 import BeautifulSoup
import math
import requests
import time
import datetime


def write_to_log(duration):
    with open('log.txt', 'a') as f:
        f.write(f'Successfully scraped data in {duration} seconds. Date: {str(datetime.datetime.now().date())}\n')


def get_urls():
    driver = webdriver.Firefox(executable_path="C:\\Users\\Chris\\Downloads\\geckodriver-v0.25.0-win64\\geckodriver.exe")
    driver.implicitly_wait(5)
    url = f'https://www.linkedin.com/jobs/search?location=Greece&trk=homepage-basic_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&f_TP=1'
    driver.get(url)

    job_count = int(driver.find_element_by_class_name('results-context-header__new-jobs').text.replace(',', '').strip('(').strip(' new)'))
    print(f'number of jobs: {job_count}')

    i=0
    while True:
        try:
            jobs = driver.find_element_by_class_name("see-more-jobs")
            time.sleep(1)
            jobs.click()
            i+=1
            print(f'button pressed {i} times')
        except Exception as e:
            print(e)
            break

    hrefs = [item.get_attribute('href') for item in driver.find_elements_by_class_name("result-card__full-card-link") if "https://gr.linkedin.com/jobs/" in item.get_attribute('href')]
    assert len(hrefs) == job_count, 'Lengths must match!'
    driver.close()
    return hrefs


class Scraper:

    def __init__(self, url):
        print('Processing: {}'.format(url))
        with requests.get(url, stream=True) as r:
            self.soup = BeautifulSoup(r.text, 'lxml')

        self.title = self.fetch_title()
        self.organization = self.fetch_organization()
        self.location = self.fetch_location()
        self.function = self.fetch_function()
        self.industry = self.fetch_industry()
        
    def fetch_title(self):
        try:
            title = self.soup.find('h1', {'class': 'topcard__title'}).text
        except Exception as e:
            title = None
        finally:
            return title
            

    def fetch_organization(self):
        try:
            organization = self.soup.find('span', {'class': 'topcard__flavor'}).text
        except Exception as e:
            organization = None
        finally:
            return organization


    def fetch_location(self):
        try:
            location = self.soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'}).text
        except Exception as e:
            location = None
        finally:
            return location


    def fetch_function(self):
        try:
            function = ','.join([item.text for item in self.soup.find_all('li', {'class': 'job-criteria__item'})[2].find_all('span')])
        except Exception as e:
            function = None
        finally:
            return function


    def fetch_industry(self):
        try:
            industry = ','.join([item.text for item in self.soup.find_all('li', {'class': 'job-criteria__item'})[3].find_all('span')])
        except Exception as e:
            industry = None
        finally:
            return industry

    def details(self):
        return {'title': self.title, 'organization': self.organization, 'location': self.location, 'function': self.function, 'industry': self.industry}
