import BeautifulSoup 
import numpy as np
from pprint import pprint

def make_fips_dict():
    import csv
    from collections import defaultdict
    from pprint import pprint

    fips_codes = defaultdict(dict)
    with open("US_FIPS_Codes.csv", "rU") as f:
        dr = csv.DictReader(f)
        for row in dr:
            fips_codes[row['State']][row['County Name']] = \
                row['FIPS State'] + row['FIPS County'].zfill(3)

def county_map_edit(filename, data):
    with open(filename) as f:
        svg = f.read()
    soup = BeautifulSoup.BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
    paths = soup.findAll('path')
    colors = ["#ffffe5",
            "#fff7bc",
            "#fee391",
            "#fec44f",
             "#fe9929",
             "#ec7014",
              "#cc4c02",
              "#993404",
            "#662506"]
            
    path_style ='font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
    
    # prepare the numbers
    # we're going to have a dictionary of counties and 
    # rates indexed by fips number
    rates_array = np.array(data.values())
    points = np.linspace(100, 0, 10)[1:-1]
    print points
    percentiles = np.percentile(rates_array, list(points))
    print "percentiles:\n", percentiles

    for p in paths:
 
        if p['id'] not in ["State_Lines", "separator"]:
            # pass
            try:
                rate = data[p['id']]
            except: 
                continue
            
            for color, percentile in zip(colors, percentiles):
                if rate > percentile:
                    color_class = color
                    break
            else:
                color = colors[0]
     
            p['style'] = path_style + color
 
    #print soup.prettify()

if __name__ == "__main__":
    import json
    with open("test_cty.json", "rb") as f:
        data = json.load(f).values()[0]
    county_map_edit('USA_Counties_with_FIPS_and_names.svg', data)
