################################################################################
#   Script for getting all recipe URLS from foodnetwork.com                    #
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
page_base = "https://www.foodnetwork.com/search/p/"
custom_facet = "/CUSTOM_FACET:RECIPE_FACET"

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
    return soup.find("span", {"class": "o-SearchStatistics__a-MaxPage"}).text.split()[1].replace(",","")

###############################################

# Get all recipe URLs from page soup object
def getrecipeurls(soup):
    recipe_links = []
    
    recipes_found = soup.find_all("section", {"class": "o-RecipeResult"})

    for a in recipes_found:
        link = a.find("a", href=True)
        recipe_links.append(link["href"])
    return recipe_links
###############################################


if __name__ == "__main__":
    page_counter = 1

    current_page = getpage(f"{page_base}{page_counter}{custom_facet}")
    total_pages = gettotalpages(current_page)

    for i in range(page_counter, 5):

        current_page = getpage(f"{page_base}{i}{custom_facet}")
        current_page_recipe_list = getrecipeurls(current_page)

        for recipe in current_page_recipe_list:
            f = open("./fn_recipes_urls.txt", "a")
            f.write(recipe)
            f.write("\n")
            f.close()