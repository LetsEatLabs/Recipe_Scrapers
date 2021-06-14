package main

//
// Imports
//

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

// A structure for each recipe.
type Recipe struct {
	id string
	url string
	title string
	author string
	description string
	level string
	totalTime int
	prepTime int
	inactiveTime int
	cookTime int
	yield string
	ingredients string
	directions string
}

// Load all lines from a file into a []string. and returns []string
func loadFileLines(filename string) []string {
	file, err := os.ReadFile(filename)

	if err != nil {
		log.Fatal(err)
	}

	content := string(file)
	lines := strings.Split(content, "\n")

	return lines

}

// Returns the MD5 sum of the entered string as a string
func hashString(str string) string {
	bytesHash := md5.Sum([]byte(str))
	stringHash := hex.EncodeToString(bytesHash[:])
	return stringHash
}

// Returns a string with only letters and numbers
func cleanString(s string) string {
	reg, err := regexp.Compile("[^a-zA-Z0-9 ]+")

	if err != nil {
		log.Println("Problem with cleaning the string", s, err)
	}

	cleanString := reg.ReplaceAllString(s, "")
	cleanString = strings.TrimSpace(cleanString)

	return cleanString
}

// Takes a URL and returns a goquery document object
func getUrlContent(url string) *goquery.Document {

	// HTTP get
	response, err := http.Get(url)
	if err != nil {
		log.Println(err)
	}

	// Close the HTTP request later, to be polite
	defer response.Body.Close()

	// Turn the raw HTTP response from the site into a goquery response object
	document, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Println("There was an error loading the HTTP body for URL", url, err)
	}

	return document

}

//
// Functions for getting data out of the html
//

// Get the title of the recipe
func getRecipeTitle(doc *goquery.Document) string {
	title := doc.Find("span[class=o-AssetTitle__a-HeadlineText]").First().Text()
	title = strings.TrimSpace(title)
	title = cleanString(title)
	return title
}

// Get the author of the recipe
func getRecipeAuthor(doc *goquery.Document) string {
	name := doc.Find("span[class=o-Attribution__a-Name] a").First().Text()
	name = cleanString(name)
	return name
}

// Get the description of the recipe
func getRecipeDescription(doc *goquery.Document) string {
	description := doc.Find("div[class=o-AssetDescription__a-Description]").First().Text()
	description = strings.TrimSpace(description)
	return description
}

// Get the level of the recipe
func getRecipeLevel(doc *goquery.Document) string {
	level := doc.Find("ul[class=o-RecipeInfo__m-Level] span[class=o-RecipeInfo__a-Description]").First().Text()
	level = strings.TrimSpace(level)
	return level
}

// Takes in a pointer to an empty Recipe struct
// And fills out every value.
func collectRecipe(recipeObj *Recipe, url string) *Recipe {

	// Set what we can set immediately
	recipeObj.id = hashString(url)
	recipeObj.url = url

	log.Println("Fetching recipe at", url)

	// Get goquery document from recipe URL
	doc := getUrlContent(url)

	// Get recipe title, author, etc
	recipeObj.title = getRecipeTitle(doc)
	recipeObj.author = getRecipeAuthor(doc)
	recipeObj.description = getRecipeDescription(doc)
	recipeObj.level = getRecipeLevel(doc)

	log.Printf("Successfully collected recipe %s (%s)", recipeObj.title, recipeObj.id)

	return recipeObj

}

//
// Main
//

func main() {

	// Check for filename argument
	if len(os.Args) != 2 {
		fmt.Println("You need to pass a single filename for the links.")
		fmt.Println("Ex: ./get-fn-recipes recipeslinks.txt")
		os.Exit(1)
	}
	// Initialize
	log.Println("Starting up Foodnetwork Website Recipe Downloader v0.1")
	targetLinks := loadFileLines(os.Args[1])
	log.Println(fmt.Sprintf("Loaded a total of %d links from file %s", len(targetLinks), os.Args[1]))

	for line := range targetLinks {
		newRecipe := &Recipe{}

		// Sometimes the URLs in the file pick up \r if on Windows >.>
		url := strings.ReplaceAll(targetLinks[line], "\r", "")
		url = fmt.Sprintf("https://%s", url)
		
		recipe := collectRecipe(newRecipe, url)

		fmt.Println(recipe)

		os.Exit(0)


	}

}