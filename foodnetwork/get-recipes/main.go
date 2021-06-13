package main

// Imports
import (
	"fmt"
	"log"
	"os"
	"strings"
)

func loadFileLines(filename string) []string {
	file, err := os.ReadFile(filename)

	if err != nil {
		log.Fatal(err)
	}

	content := string(file)
	lines := strings.Split(content, "\n")

	return lines

}

//func getUrlContent(url string) {}

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
		fmt.Println(targetLinks[line])
	}

}