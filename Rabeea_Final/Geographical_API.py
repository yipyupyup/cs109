# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests
from BeautifulSoup import BeautifulSoup

# <codecell>

COUNTRY_DICT = {}

# <codecell>

def create_country_data():
    country_data_url = "http://www.geonames.org/countries/"
    country_data = requests.get(country_data_url).text
    soup = BeautifulSoup(country_data)
    for link_tag in soup.findAll('a'):
        if link_tag.has_key('href'):
            link = link_tag['href']
            if link[0:11] == '/countries/':
                COUNTRY_DICT[link[11:13]] = link[14:-5]

# <codecell>

create_country_data()

# <codecell>

def country_from_code(code):
    return COUNTRY_DICT[code]

# <codecell>

def get_location(longitude, latitude):
    web_url = "http://ws.geonames.org/countryCode?lat="+str(latitude)+"&lng="+str(longitude)
    country_code = requests.get(web_url).text
    country_name = country_from_code(country_code)
    print country_name

# <codecell>


# <codecell>


# <codecell>

get_location(73.06, 33.71)

# <codecell>


