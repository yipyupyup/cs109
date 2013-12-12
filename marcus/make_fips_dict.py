import csv
from collections import defaultdict
from pprint import pprint

fips_codes = defaultdict(dict)
with open("US_FIPS_Codes.csv", "rU") as f:
	dr = csv.DictReader(f)
	for row in dr:
		fips_codes[row['State']][row['County Name']] = \
			row['FIPS State'] + row['FIPS County'].zfill(3)

pprint(fips_codes)