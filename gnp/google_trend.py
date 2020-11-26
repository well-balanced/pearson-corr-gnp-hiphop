from pytrends.request import TrendReq
from utils import load_data_as_dict, export_as_csv
import pandas as pd
import csv
import os

def main():
    pytrends = TrendReq(hl='en')
    keywords = ['Hip hop music', 'Jazz',]
    start_date = '2017-01-01'
    end_date = '2017-12-31'
    gnp_dict = load_data_as_dict('gnp.csv')
    iso_code_arr = gnp_dict.keys()

    top_suggestions = list(map(lambda x: pytrends.suggestions(x)[0]['mid'], keywords))
    preference_dict = dict()

    for iso_code in iso_code_arr:
        results = fetch_trend_results(pytrends, top_suggestions, iso_code, start_date, end_date)
        results.to_csv('trends/{}.csv'.format(iso_code), encoding='utf-8')
        preference_score = get_preference_score(iso_code)
        preference_dict[iso_code] = preference_score 

    # remove outliers and export as csv
    filtered_dict = {key: value for key, value in preference_dict.items() if value is not None}
    sanitized_dict = {key: value  for key, value in gnp_dict.items() if key in filtered_dict.keys()}
    export_as_csv('preference.csv', filtered_dict)
    export_as_csv('gnp.csv', sanitized_dict)

def fetch_trend_results(pytrends, keywords: list, iso_code: str, start_date: str, end_date: str):
    """
    Fetch preference datas using Google Trends API
    """
    pytrends.build_payload(
      keywords, 
      cat=0, 
      timeframe='{} {}'.format(start_date, end_date), 
      geo=iso_code,
      gprop='',
    )
    results = pytrends.interest_over_time()
    if 'isPartial' in results.keys():
        del results['isPartial']
    return results

def get_preference_score(iso_code: str) -> float or int or None:
    """
    Extract a Preference score from a CSV data
    """
    with open('trends/{}.csv'.format(iso_code)) as file:
        reader = csv.reader(file, delimiter=';')
        count = 0
        aggregate = 0
        for idx, row in enumerate(reader):
            values = row[0].split(',')
            try:
                hiphop_score = int(values[1])
                jazz_score = int(values[2])
                rate = hiphop_score / jazz_score
                aggregate += rate
                count += 1
            except ValueError:
                pass
            except ZeroDivisionError:
                print('assumed that target country has outliers. except "{}"'.format(iso_code))
                return None
            except IndexError:
                print('google trends do not support this iso code {}'.format(iso_code))
                return None
    preference_score = round(aggregate / count, 2)
    return preference_score

main()