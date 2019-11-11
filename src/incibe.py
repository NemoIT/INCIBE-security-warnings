
import requests
import json
import time
from bs4 import BeautifulSoup
import os
import constants


class INCIBEScraper():

    def __init__(self):
        self.data = {}
        self.data['articles'] = []
        self.URL = constants.INCIBE_BASE_URL + constants.INCIBE_REL_HOME_URL
        self.more_pages = True
        self.count = 0

    def scrape(self):

        print('Wellcome to INCIBE scraper')

        while self.more_pages and self.count < 2:

            page = requests.get(self.URL)

            print("\nReading " + self.URL + "...", end='')

            soup = BeautifulSoup(page.text, 'html.parser')

            for article in soup.find_all(name='article', attrs={'class': 'node'}):

                self.count = self.count + 1

                item_title = article.header.text.strip()
                item_date = article.footer.text.strip()

                severity = article.find(
                    name='span', attrs={'class': 'level-text'})
                item_severity = severity.text.strip().replace('\t', '')

                item_labels = []

                labels = article.find(
                    name='div', attrs={'class': 'field-name-field-etiquetas'})

                for label in labels.find_all(name='div', attrs={'class': 'field-item'}):
                    item_labels.append(label.a.text)

                time.sleep(constants.SCRAPING_DELAY_SHORT)
                page_detail = requests.get(
                    constants.INCIBE_BASE_URL + article.header.a['href'])
                soup_detail = BeautifulSoup(page_detail.text, 'html.parser')

                descripcion = soup_detail.find(name='div', attrs={
                                               'class': 'field-name-field-descripcion'}).find(name='div', attrs={'class': 'field-item'}).text.strip()
                solucion = soup_detail.find(name='div', attrs={
                                            'class': 'field-name-field-solucion'}).find(name='div', attrs={'class': 'field-item'}).text.strip()

                self.data['articles'].append({
                    'title': item_title,
                    'date': item_date,
                    'severity': item_severity,
                    'labels': item_labels,
                    'description': descripcion,
                    'solution': solucion
                })

            pager_next = soup.find(name='li', attrs={'class': 'pager-next'})


            if (pager_next == None):
                self.more_pages = False
            else:
                self.more_pages = True
                self.URL = constants.INCIBE_BASE_URL + pager_next.a['href']
                time.sleep(constants.SCRAPING_DELAY_LONG)

        print('\nDone!')



    def save2json(self, filename):

        with open(filename, 'w') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=4)

        
        print(str(self.count) + ' alerts scraped. Saved to ' + os.getcwd() + '\\' + filename)
        
