import matplotlib.pyplot as plt
import json
from collections import defaultdict
import numpy as np

from utils.plot import plot_cases, plot_growth, plot_deaths
from utils.country_data import compute_countries_confirmed_cases,compute_countries_confirmed_deaths
from utils.growth_rate import compute_growth_rate

ALIGN_AROUND_CASES = 400 # cases
ALIGN_AROUND_DEATHS = 20  # deaths

if __name__ == "__main__":
    # Compute the number of cases for each country
    confirmed = compute_countries_confirmed_cases()
    deaths = compute_countries_confirmed_deaths()

    # Compute maximum number of cases we can align around: min (ALIGN_AROUND, x)
    # Take the second biggest one
    minimums = [sorted(v)[-2] for c, v in confirmed.items()]
    minimum_deaths = [sorted(v)[-2] for c, v in deaths.items()]
    new_align_around = np.minimum(ALIGN_AROUND_CASES, np.min(minimums))
    new_align_deaths = np.minimum(ALIGN_AROUND_DEATHS, np.min(minimum_deaths))
    print(new_align_deaths)

    # Compute the index for each country in order to align around the same number of cases
    align_indexes_cases = defaultdict(list)
    for c, v in confirmed.items():
        dist = np.abs(np.array(v) - new_align_around)
        align_indexes_cases[c] = np.argmin(dist)

    align_indexes_deaths = defaultdict(list)
    for c, v in deaths.items():
        dist = np.abs(np.array(v) - new_align_deaths)
        align_indexes_deaths[c] = np.argmin(dist)

    growths = compute_growth_rate(confirmed)

    plot_cases(confirmed, align_indexes_cases, new_align_around)
    plot_deaths(deaths, align_indexes_deaths, new_align_deaths)
    plot_growth(growths, align_indexes_cases, new_align_around)
