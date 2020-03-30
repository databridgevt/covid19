import os

import bs4 
from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen



'''
Scrapes drugbank.ca for antivirals and writes a pdb file. 
search_page: a string of the initial search result URL. 
'''
class DrugbankScraper:
    def __init__(self, search_page):
        
        self.search_pages = []

        # get additional search pages
        search_page_parts = search_page.split('&')
        if 'page=' in search_page_parts:
            all_pages = self.getPages(search_page, 8)
            for item in all_pages:
                self.search_pages.append(item)

        # get html      
        for page in self.search_pages:
            
            url = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
            uClient = urlopen(url)
            html = uClient.read()
            page_soup = soup(html, 'html.parser')
            
            # get drug data
            links = page_soup.find_all('h2', {'class':'hit-link'})
            for link in links:
                # find accession number
                href = link.a.attrs['href']
                href_parts = href.split('/')
                accession_number = href_parts[2]
                # get drug info page
                print(accession_number)
                info_page = 'https://drugbank.ca/drugs/' + accession_number
                info_url = Request(info_page, headers={'User-Agent': 'Mozilla/5.0'})
                uClient2 = urlopen(info_url)
                html = uClient2.read()
                info_soup = soup(html, 'html.parser')
                # get drug name
                name = info_soup.dd.text
                # get pdb file
                download_page = 'https://drugbank.ca/structures/small_molecule_drugs/' + accession_number + '.pdb'
                download_url = Request(download_page, headers={'User-Agent': 'Mozilla/5.0'})
                uClient3 = urlopen(download_url)
                pdb = uClient3.read()
                pdb_soup = soup(pdb, 'html.parser')
                # download pdb
                self.download(pdb_soup, name)

    # given a url and max number of pages, return a list of search result pages
    def getPages(self, link, max):
        links = []
        link_parts = link.split('&')
        i = 2
        string = ''
        index = len(links) - 1
        while i <= max:
            link_parts[2] = 'page=' + str(i)
            for part in link_parts:
                if part == link_parts[index]:
                    string = string + part
                else:
                    string = string + part + '&'
            links.append(string)
            string = ''
            i += 1
        return links

    # download pdb file
    def download(self, html, name):
        filname = name + '.pdb'
        f = open(filname, 'w')
        f.write(str(html))
        f.close()
        


scraper = DrugbankScraper(search_page='https://www.drugbank.ca/unearth/q?c=_score&d=down&page=1&query=antiviral&searcher=drugs')

