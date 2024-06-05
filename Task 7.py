import requests
from requests.exceptions import ConnectTimeout, HTTPError

class CountryData:
    def __init__(self, url):
        self.url = url
        self.data = self.fetch_data()

    def fetch_data(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.json()
        except ConnectTimeout:
            print("Connection timed out. Please check your internet connection or try again later.")
            return []
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"An error occurred: {err}")
            return []

    def display_countries_currencies(self):
        for country in self.data:
            name = country.get('name', {}).get('common', 'Unknown')
            currencies = country.get('currencies', {})
            for currency_code, currency_info in currencies.items():
                currency_name = currency_info.get('name', 'Unknown')
                currency_symbol = currency_info.get('symbol', 'Unknown')
                print(f"Country: {name}, Currency: {currency_name}, Symbol: {currency_symbol}")

    def countries_with_currency(self, currency_name):
        countries = [country.get('name', {}).get('common', 'Unknown') for country in self.data if currency_name in {cur.get('name', '') for cur in country.get('currencies', {}).values()}]
        return countries

    def display_dollar_countries(self):
        dollar_countries = self.countries_with_currency('Dollar')
        print("Countries using Dollar as their currency:")
        for country in dollar_countries:
            print(country)

    def display_euro_countries(self):
        euro_countries = self.countries_with_currency('Euro')
        print("Countries using Euro as their currency:")
        for country in euro_countries:
            print(country)

# URL for country data
url = "https://restcountries.com/v3.1/all"
country_data = CountryData(url)
if country_data.data:
    country_data.display_countries_currencies()
    country_data.display_dollar_countries()
    country_data.display_euro_countries()

class BreweryData:
    def __init__(self, url):
        self.url = url
        self.data = self.fetch_data()

    def fetch_data(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.json()
        except ConnectTimeout:
            print("Connection timed out. Please check your internet connection or try again later.")
            return []
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return []
        except Exception as err:
            print(f"An error occurred: {err}")
            return []

    def filter_breweries_by_state(self, states):
        return [brewery for brewery in self.data if brewery['state'] in states]

    def list_breweries(self, states):
        breweries = self.filter_breweries_by_state(states)
        for brewery in breweries:
            print(brewery['name'])

    def count_breweries_by_state(self, states):
        breweries = self.filter_breweries_by_state(states)
        state_counts = {state: 0 for state in states}
        for brewery in breweries:
            state_counts[brewery['state']] += 1
        return state_counts

    def count_brewery_types_by_city(self, state):
        breweries = [brewery for brewery in self.data if brewery['state'] == state]
        city_brewery_types = {}
        for brewery in breweries:
            city = brewery['city']
            brewery_type = brewery['brewery_type']
            if city not in city_brewery_types:
                city_brewery_types[city] = {}
            if brewery_type not in city_brewery_types[city]:
                city_brewery_types[city][brewery_type] = 0
            city_brewery_types[city][brewery_type] += 1
        return city_brewery_types

    def breweries_with_websites(self, states):
        breweries = self.filter_breweries_by_state(states)
        breweries_with_websites = [brewery for brewery in breweries if brewery['website_url']]
        return breweries_with_websites

# URL for brewery data
brewery_url = "https://api.openbrewerydb.org/breweries"
brewery_data = BreweryData(brewery_url)

# States of interest
states = ['Alaska', 'Maine', 'New York']

if brewery_data.data:
    # List names of all breweries in Alaska, Maine, and New York
    brewery_data.list_breweries(states)

    # Count of breweries in each of the states mentioned above
    brewery_counts = brewery_data.count_breweries_by_state(states)
    print("Brewery counts by state:", brewery_counts)

    # Count the number of types of breweries present in individual cities of the states mentioned above
    for state in states:
        city_brewery_types = brewery_data.count_brewery_types_by_city(state)
        print(f"Brewery types by city in {state}:", city_brewery_types)

    # Count and list how many breweries have websites in the states of Alaska, Maine, and New York
    breweries_with_websites = brewery_data.breweries_with_websites(states)
    print("Breweries with websites:")
    for brewery in breweries_with_websites:
        print(brewery['name'], brewery['website_url'])
