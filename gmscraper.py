#! /usr/bin/env python3

'''
Copyright (C) 2019
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import requests, json, time
import pandas as pd
import numpy as np
import argparse

# Begin construction of the parser to handle command line 
# options and display help text

parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='''Scrape Google Maps for locations matching a given
keyword within a specified radius of set coordinates''',
                prog='Google Maps Scraper',
                usage='gmscraper [coordinates] [radius] [keyword]',
                epilog=('''\
example:

gmscraper -c '38.897626180055525, -77.03679802300508' -r 5000 -k 'restaurant'

gmscraper [no arguments] - returns all restaurants within 1KM of the White House

NOTES:

- Get the coordinates from Google Maps for the center of your search area.

- The radius is in meters. Five miles is approximately 8000 meters, this 
would return a search area 10 miles in diameter.

- Google has a limit of 60 returns for a search, so making the radius
too large will result in an incomplete listing for certain things like
restaurants.

- An API key is required to scrape Google Maps. 
You can create a key with a developer account at https://cloud.google.com/

- Since this program was created to be used on a local machine, the API
key is in the code. Just paste yours as the value of api_key = 'your_key' in the code.
DO NOT hard code your key in a public facing production environment.
If you're doing that you know how to protect your key and are likely not
using this script to begin with.\n\n
''')
                )

parser.add_argument('--coordinates', '-c', default='38.897626180055525, -77.03679802300508', help='Coordinates for center of search area')
parser.add_argument('--radius', '-r', default=1000, help='Radius of search area (default is 1000 meters)'),
parser.add_argument('--keyword', '-k', default='restaurant', help='Search keyword. (Default is restaurant)')

args = parser.parse_args()

# End parser construction

# enter your api key here
api_key = ''

coordinates = args.coordinates
keyword = args.keyword
radius = args.radius
final_data = []

# url variable store url
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+coordinates+'&radius='+str(radius)+'&keyword='+str(keyword)+'&key='+str(api_key) 

# Perform the search until there are no more results available.
# Each search returns up to 20 results. The search will be performed
# a maximum of 3 times (limit set by Google)

while True:
    print(url)
    response = requests.get(url)
    jj = json.loads(response.text)
    results = jj['results']
    for result in results:
        name = result['name']  # Extract the name of the location from the results
        vicinity = result['vicinity']  # Extract the address from the results
        data = [name, vicinity]
        final_data.append(data) # Append the name and location to the full list

    time.sleep(5)
    
    # If no further pages of results are found, stop the search.
    # If there is another page of results, perform the search again
    # with the next page token

    if 'next_page_token' not in jj:
        break

    else:
            next_page_token = jj['next_page_token']
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+str(api_key)+'&pagetoken='+str(next_page_token)

# Displays a formatted table to stout with names and addresses
# using Pandas

labels = ['Name', 'Address']
display = pd.DataFrame.from_records(final_data, columns=labels)
print(display)
print()
print()

# Uncomment to dump the contents of the final_data variable to a file
# to copy as a nested list variable for another program.

'''
with open('restaurants.py', 'w') as f:
        json.dump(final_data, f)
'''

# Uncomment to print the final results of the search directly 
# to the terminal

'''
for i in final_data:
        print('\n'.join(i))
'''
