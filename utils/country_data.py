from collections import defaultdict
import json
import sys
import requests
import os
import time

# Generate population structure from file
population = 'country-by-population.json'
if os.path.exists(population):
    with open(population) as json_pop_file:
        pop_data = json.load(json_pop_file)

countries = {}
for item in pop_data:
    countries.update({item['country']: item['population']})

ts_url = "https://pomber.github.io/covid19/timeseries.json"
local_f = 'timeseries.json'

if os.path.exists(local_f):
    # If timeseries file exists but is older than a day, download it again
    if os.stat(local_f).st_mtime < time.time() - 86400:
        data = requests.get(ts_url).json()
        with open(local_f, 'w') as outfile:
            json.dump(data, outfile)
# if timeseries doesn't exist at all, download it
else:
    data = requests.get(ts_url).json()
    with open(local_f, 'w') as outfile:
        json.dump(data, outfile)

with open(local_f) as json_file:
    data = json.load(json_file)


def parse_countries() -> list:
    countries = list(data.keys())

    default_countries = ["Spain", "Italy", "United Kingdom", "US", "France",
                         "Netherlands", "Turkey", "Belgium", "Iran", "Germany",
                         "China"]
    all_countries = list()

    new_countries = sys.argv[1:]
    new_countries = list(filter(lambda x: x in countries, new_countries))

    all_countries.extend(default_countries)
    all_countries.extend(new_countries)
    return all_countries


def compute_countries_confirmed_cases() -> dict:

    # Get all data for each country
    all_countries = parse_countries()
    confirmed = defaultdict(list)

    for c in all_countries:
        local_data = [d.get("confirmed") for d in data[c]]
        # Clean when there are dates with no update and a "sudden" jump
        new_local_data = list()

        for idx, d in enumerate(local_data):
            if idx > 1 and idx < len(local_data) \
               and d - local_data[idx-1] == 0:
                new_local_data.append((local_data[idx-1] + local_data[idx+1])
                                      / 2)
            else:
                new_local_data.append(d)

        confirmed[c] = new_local_data
    return confirmed


def compute_countries_confirmed_deaths() -> dict:

    # Get all data for each country
    all_countries = parse_countries()
    deaths = defaultdict(list)

    for c in all_countries:
        local_data = [d.get("deaths") for d in data[c]]
        # Clean when there are dates with no update and a "sudden" jump
        new_local_data = list()

        foo = "true"
        for idx, d in enumerate(local_data):
            try:
                local_data[idx+1]
            except IndexError:
                foo = None
            if idx > 1 and idx < len(local_data) \
               and d - local_data[idx-1] == 0 \
               and foo is not None:
                new_local_data.append((local_data[idx-1] + local_data[idx+1])
                                      / 2)
            else:
                new_local_data.append(d)

        deaths[c] = new_local_data
    return deaths


def compute_countries_confirmed_deaths_per_population() -> dict:

    # Get all data for each country
    all_countries = parse_countries()
    deaths = defaultdict(list)

    for c in all_countries:
        try:
            print("Country: %s, Population: %s" % (c, countries[c]))
        except KeyError:
            pass
        local_data = [d.get("deaths") for d in data[c]]
        # Clean when there are dates with no update and a "sudden" jump
        new_local_data = list()

        for idx, d in enumerate(local_data):
            if idx > 1 and idx < len(local_data) \
               and d - local_data[idx-1] == 0:
                try:
                    new_local_data.append((local_data[idx-1] +
                                          local_data[idx+1]) /
                                          2 * 100 /
                                          int(countries[c]))
                except KeyError:
                    pass
            else:
                new_local_data.append(d * 100 / int(countries[c]))

        deaths[c] = new_local_data
    return deaths
