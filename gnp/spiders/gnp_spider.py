import scrapy
import pycountry
from functools import reduce
import csv
from utils import export_as_csv

class GNPSpider(scrapy.Spider):
    """
    Scrape GNP information using lib 'Scrapy'
    """
    name = "gnp"
    start_urls = ['https://www.worldometers.info/gdp/gdp-per-capita/']

    def parse(self, response):
      arr_included_gnp_info = extract_gnp_info(response)
      country_gnp_dict = map_country_gnp(arr_included_gnp_info)
      iso_code_gnp_dict = parse_country_to_iso_code(country_gnp_dict)
      export_as_csv('gnp.csv', iso_code_gnp_dict)



def extract_gnp_info(response) -> list:
  """
  Return GNP information extracted from the unrefined HTML response.
  + Crawling rank between 1 and 100
  """
  arr_included_gnp = []

  for i in range(1, 101):
    for row in response.css('#example2 tbody tr:nth-child({})'.format(i)):
      arr_included_entity = []

      for j in range(0, 4):
        for col in row.css('td:nth-child({})'.format(j)):
          arr_included_entity.append(col.css('::text').extract()[0])

      arr_included_gnp.append(arr_included_entity)
  
  return arr_included_gnp


def map_country_gnp(arr_included_gnp_info: list) -> dict:
  """
  Combine country with GNP
  """
  country_gnp_dict = {}
  for obj in arr_included_gnp_info:
    country = obj[1]
    gnp = obj[2]
    parsed_gnp = gnp.strip().replace('$', '').replace(',', '')
    country_gnp_dict[country] = parsed_gnp
  return country_gnp_dict


def parse_country_to_iso_code(country_gnp_dict: dict) -> dict:
  """
  Replace country with iso code
  """
  iso_code_gnp_dict = {}
  for country in list(pycountry.countries):
    if country.name in country_gnp_dict.keys():
      iso_code_gnp_dict[country.alpha_2] = country_gnp_dict[country.name]
      del country_gnp_dict[country.name]
  redeemed_dict = append_omitted_country(iso_code_gnp_dict, country_gnp_dict)
  return redeemed_dict


def append_omitted_country(iso_code_gnp_dict: dict, country_gnp_dict: dict) -> dict:
  """
  Redeem a dict with ommitted values
  """
  iso_code_gnp_dict['BN'] = country_gnp_dict['Brunei ']
  iso_code_gnp_dict['KR'] = country_gnp_dict['South Korea']
  iso_code_gnp_dict['CZ'] = country_gnp_dict['Czech Republic (Czechia)']
  iso_code_gnp_dict['KN'] = country_gnp_dict['Saint Kitts & Nevis']
  iso_code_gnp_dict['RU'] = country_gnp_dict['Russia']
  iso_code_gnp_dict['IR'] = country_gnp_dict['Iran']
  return iso_code_gnp_dict
