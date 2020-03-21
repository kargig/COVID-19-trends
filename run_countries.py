import matplotlib.pyplot as plt
import json
from collections import defaultdict
import numpy as np

from utils.plot import plot_cases, plot_growth, plot_deaths
from utils.country_data import compute_countries_confirmed_cases,compute_countries_confirmed_deaths
from utils.growth_rate import compute_growth_rate

ALIGN_AROUND_CASES = 400 # cases
ALIGN_AROUND_DEATHS = 5  # deaths

if __name__ == "__main__":
    # Compute the number of cases for each country
    confirmed = compute_countries_confirmed_cases()
    deaths = compute_countries_confirmed_deaths()

    # Compute the index for each country in order to align around the same number of cases
    align_indexes_cases = defaultdict(list)
    for c, v in confirmed.items():
        dist = np.abs(np.array(v) - ALIGN_AROUND_CASES)
        align_indexes_cases[c] = np.argmin(dist)

    align_indexes_deaths = defaultdict(list)
    for c, v in confirmed.items():
        dist = np.abs(np.array(v) - ALIGN_AROUND_DEATHS)
        align_indexes_deaths[c] = np.argmin(dist)


    growths = compute_growth_rate(confirmed)

    plot_cases(confirmed, align_indexes_cases, ALIGN_AROUND_CASES)
    plot_deaths(deaths, align_indexes_deaths, ALIGN_AROUND_DEATHS)
    plot_growth(growths, align_indexes_cases, ALIGN_AROUND_CASES)
