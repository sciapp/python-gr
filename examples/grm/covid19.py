#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

import grm
import numpy as np
import requests

COUNTRIES = ["Germany", "Austria", "Belgium", "Netherlands", "France", "Italy", "Spain", "US"]
COVID_DATA_URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
    "master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
)


def main():
    reponse = requests.get(COVID_DATA_URL)
    covid_data = reponse.content.decode("utf-8")
    covid_reader = csv.reader(covid_data.splitlines(), delimiter=",")
    fieldnames = next(covid_reader)
    number_of_days = len(fieldnames) - 4
    days = np.arange(number_of_days, dtype=np.float64)
    confirmed = {
        row[1]: np.fromiter((int(n) for n in row[4:]), dtype=np.float64) for row in covid_reader if row[1] in COUNTRIES
    }

    args = grm.args.new(
        {
            "series": [
                {
                    "x": days,
                    "y": confirmed[country],
                }
                for country in COUNTRIES
            ],
            "x_lim": (0.0, number_of_days + 1.0),
            "y_lim": (10.0, 20_000_000.0),
            "y_log": 1,
            "title": "Confirmed SARS–CoV–2 infections",
            "x_label": "Day",
            "y_label": "Confirmed",
            "labels": COUNTRIES,
            "location": 4,
        }
    )
    grm.plot.plot(args)

    print("Press any key to continue...")
    input()

    grm.plot.finalize()


if __name__ == "__main__":
    main()
