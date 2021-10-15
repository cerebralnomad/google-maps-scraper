# google-maps-scraper
Scrape Google Maps for locations matching a given keyword within a specified radius of set coordinates

## Installation

Create a virtualenv for the project unless you already have the dependancies installed  
or want to install them globally, and clone this repo into it.  
The packages and modules required for running the script are:  

requests  
json  
time  
pandas  
numpy  
argparse  

They are listed in the requirements.txt file.

## API Key

You will have to have an API key for Google Maps Places to use this script.   
You can create a key with a Google Cloud Developer account at https://cloud.google.com/.  
A recent requirement of Google is that you have a form of payment on file before a key can be enabled.  
Use of the key however is basically free for personal use as Google will apply a monthly credit  
of $200 to your accoun, which will cover pretty much any amount of non-commercial use.

## Usage

Since this script was designed for personal use and to be run locally, the API key is hard coded into the file.  
You'll need to edit gmscraper.py with Vim or a GUI text editor and add your API key on line 68.  
The line will look like:  

    api_key = 'your_api_key'
    
Run the script with the necessary options: coordinates, radius, and keyword.  

    gmscraper -c 'coordinates' -r [radius] -k [keyword]
    
For example:

    gmscraper -c '38.897626180055525, -77.03679802300508' -r 1000 -k 'restaurant'
    
The above coordinates are for the White House in Washington D.C.  
This command is the default and will return a list of all restaurants within 1000 meters of the White House.

Retreve the full help text with:

    gmscraper -h
    
## Options

By default the script will display the results of the search in a table directly in the terminal.

Two blocks of code are commented out.  
One block dumps the results of the search into a file 'search_results.py' in the form of a nested list.  
This can be copied and used as the value of a variable in another program.  
The other block prints the search results directly to the terminal.  

