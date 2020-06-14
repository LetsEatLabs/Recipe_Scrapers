################################################################################
#   Script for getting recipes from tasteofhome.com                            #
#   and combining them into a csv file                                         #
#                                                                              #
#   Written by: Jeremy Heckt, Let's Eat Labs - Scientist                       #
#   June, 2020, LC, Seattle, WA                                                #
################################################################################

import importlib

# Get our other file so we do not have to re-write code
getlinks = importlib.import_module("getlinks")

# Define some stuff
page_base = "https://www.tasteofhome.com/search/index?search=&page="

# Open our list of recipes
test_recipe_list = open("test_recipes.txt", "r")
real_recipe_list = open("recipes_urls.txt", "r")

####################

def extractrecipe(soup, target_class, target_type):
    return soup.find_all(target_type, {"class": target_class})

####################

####################

def cleanrecipeline(line_text):
    return line_text.replace(",","")

####################

####################

def getfullingredients(url):
    """
    Returns an string of all recipe ingredients and the sub recipes if present
    comma separated
    """
    url_soup = getlinks.getpage(url)
    url_recipe = extractrecipe(url_soup, 
                    "recipe-ingredients__collection", 
                    "ul")
    ingredient_list = []
    for ingredient in url_recipe:
        for line in ingredient.find_all("li"):
            ingredient_list.append(line.text)
    return ",".join(ingredient_list).replace(":,",": ")

####################

for url in test_recipe_list.readlines():
    print(getfullingredients(url))














