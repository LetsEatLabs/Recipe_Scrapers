################################################################################
#   Script for getting all recipe URLS from tasteofhome.com                    #
#   and combining them into a text file                                        #
#                                                                              #
#   Written by: Jeremy Heckt, Let's Eat Labs - Scientist                       #
#   June, 2020, LC, Seattle, WA                                                #
################################################################################

import requests
import bs4 as bs
import cfscrape
import time

# Base URL
page_base = "https://www.tasteofhome.com/search/index?search=&page="

###############################################

# Get a page
def getpage(page_base,page_number=""):
    """
    Returns a soup object of the search index page
    """
    session = requests.session()
    sess = session.get(page_base)
    scraper = cfscrape.create_scraper(sess=sess)

    url_str = page_base + str(page_number)
    page = scraper.get(url_str).content

    soup = bs.BeautifulSoup(page, 'lxml')

    return soup

###############################################

# Find total number of pages
def gettotalpages(soup):
    """
    Gets the total number of index pages
    """
    pagination = soup.find_all("li", {"class": "pagination-inactive"})
    return pagination[-1].text

###############################################

# Get all recipe URLs from page soup object
def getrecipeurls(soup):
    """
    Extract the href from all recipes returned on this index page
    """
    links = soup.find_all("a", {"class": "rd_search_result_title"}, href=True)
    return list(set([x['href'] for x in links]))


###############################################

# Get total pages into variable
first_page = getpage(page_base,1)
total_pages = gettotalpages(first_page)


if __name__ == "__main__":
    page_counter = 1

    for i in range(page_counter, int(total_pages)):

        current_page = getpage(page_base,i)
        current_page_recipe_list = getrecipeurls(current_page)

        for recipe in current_page_recipe_list:
            f = open("recipes_urls.txt", "a")
            f.write(recipe)
            f.write("\n")
            f.close()

    

        



