################################################################################
#   Script for getting recipes from tasteofhome.com                            #
#   and combining them into a csv file                                         #
#                                                                              #
#   Written by: Jeremy Heckt, Let's Eat Labs - Scientist                       #
#   July, 2020, LC, Seattle, WA                                                #
################################################################################

import importlib
import json
import os
import datetime

# Get our other file so we do not have to re-write code
getlinks = importlib.import_module("getlinks")

# Define some stuff
page_base = "https://www.tasteofhome.com/search/index?search=&page="

# Source
target_source = "Taste Of Home"

# Open our list of recipes
test_recipe_list = open("test_recipes.txt", "r")
real_recipe_list = open("production_recipes_urls.txt", "r")

# Target save directory
save_dir = "./json/"

# Logfile
log_file = open("./getrecipe.log", "a")

####################

def extractfromrecipe(soup, target_class, target_type):
    return soup.find_all(target_type, {"class": target_class})

####################

####################

def cleanrecipeline(line_text):
    return line_text.replace(",","")

####################

####################

def getrecipetitle(url_soup):
    return extractfromrecipe(url_soup, "recipe-title", "h1")[0].text

####################

####################

def getrecipenutrition(url_soup):
    nutr_obj = {}

    nutrition = extractfromrecipe(url_soup, 
                    "recipe-nutrition-facts",
                    "div")[0].text
    nutrition = nutrition.strip().replace("Nutrition Facts\n\t\t", "")

    nutrition_split = nutrition.split(":")

    nutr_obj["portion"] = nutrition_split[0]
    nutr_obj["facts"] = [x.strip() for x in nutrition_split[1][:-1].split(",")]
    #[:-1] to remove trailing period

    return nutr_obj

####################

####################

def getfulldirections(url_soup):
    """
    Returns an object of all the directions
    """
    recipe_directions = extractfromrecipe(url_soup, 
                            "recipe-directions__item", 
                            "li")
    recipe_list = [x.text.strip() for x in recipe_directions]

    return recipe_list

####################

####################

def getfullingredients(url_soup):
    """
    Returns an string of all recipe ingredients and the sub recipes if present
    comma separated
    """
    url_recipe = extractfromrecipe(url_soup, 
                    "recipe-ingredients__collection", 
                    "ul")
    ingredient_list = []
    for ingredient in url_recipe:
        for line in ingredient.find_all("li"):
            ingredient_list.append(line.text)

    # Do not use commas as they use them!
    return "|".join(ingredient_list)#.replace(":,",": ")

####################

####################

def cleansubrecipe(sub_recipe_list):
    title_inds = [sub_recipe_list.index(x) for x in sub_recipe_list if ":" in x]
    sub_recipe_obj = {}

    sub_recipe_array = []
    for i in range(len(title_inds)):
        if title_inds[i] == title_inds[-1]:
            sub_recipe_array.append(sub_recipe_list[title_inds[i]:])
        else:
            sub_recipe_array.append(sub_recipe_array[title_inds[i]:title_inds[i+1]])


    for sr in sub_recipe_array:

        # Weird edge cases of Optional sub recipes
        if sr[:9] == "Optional:":
            sub_title = "Optional:"
            sub_recipe_obj[sub_title] = sr[9:]

        else:
            sub_title = sr[0].replace(":","")
            sub_recipe_obj[sub_title] = sr[1:] # Skip the title easily

    return sub_recipe_obj


####################

####################

def recipeprettify(recipe_string):
    """
    Takes comma separated recipe string returned by getfullingredients()
    and returns an object with recipe and sub-recipe, if applicable.

    "Optional:" ingredients are to be put into the sub-recipe field, but not
    ingredients listed in the main portion as optional. Note the difference:
        "Optional: " <--- subrecipe
        "walnuts, optional" <--- main recipe
    """
    split_str = recipe_string.split("|") # Do not use commas as they use them!
    recipe_obj = {}

    if ":" in recipe_string:
        colon_index = 0
        sub_recipes = []
        for r in split_str:
            if ":" in r:
                colon_index = split_str.index(r)
                sub_recipes = split_str[colon_index:] 
                break # Break so we get ALL sub recipes in one spot
        recipe_obj["recipe"] = split_str[:colon_index]
        recipe_obj["subrecipes"] = cleansubrecipe(sub_recipes)
    else:
        recipe_obj["recipe"] = split_str
    return recipe_obj

####################

####################

def writerecipe(write_file, recipe_obj, recipe_count):
    """
    Saves recipe
    """

    with open(write_file, "w") as f:
        f.write(json.dumps(recipe_obj, ensure_ascii=False))

####################

####################

def logwritter(log_file, string_message):
    log_file.write(f"{datetime.datetime.now()}|{string_message}\n")

####################

####################


if __name__ == "__main__":
    recipe_url_list = test_recipe_list.readlines()
    total_recipes = len(recipe_url_list)

    existing_recipes = os.listdir(save_dir)

    total_recipes = 0

    for url in recipe_url_list: 
        write_file = f"{save_dir}{target_source.replace(' ', '')}-{total_recipes}.json"

        ############ # Check if recipe already exists. If it does, skip.
        direct_file_name = write_file[7:]

        if direct_file_name in existing_recipes:
            logwritter(log_file, f"{direct_file_name} is already saved, skipping...")
            total_recipes += 1
            continue
        ############

        url_soup = getlinks.getpage(url)

        recipe_obj = recipeprettify(getfullingredients(url_soup))
        recipe_obj["directions"] = getfulldirections(url_soup)
        recipe_obj["title"] = getrecipetitle(url_soup)
        recipe_obj["nutrition"] = getrecipenutrition(url_soup)
        recipe_obj["url"] = url.strip()
        recipe_obj["source"] = target_source
        
        writerecipe(write_file, recipe_obj, total_recipes)
        logwritter(log_file, f"{direct_file_name} is written")
        total_recipes += 1


# To Do Next
# split sub recipes into actual subobjects for clarity. (we can leave as arrays)
# Write a script that will take all JSON files in a dir and make a giant file








