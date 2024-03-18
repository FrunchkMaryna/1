import redis
import json
import requests
import time

currency_map = {
    'US Dollar': 'USD',
    'Euro': 'EUR',
    'British Pound': 'GBP',
    'Japanese Yen': 'JPY',
    'Canadian Dollar': 'CAD',
    'Swiss Franc': 'CHF',
    'Australian Dollar': 'AUD',
    'New Zealand Dollar': 'NZD',
    'Chinese Yuan': 'CNY',
    'Indian Rupee': 'INR',
}

def get_currency_from_user():
    while True:
        currency_name = input("Enter the currency name: ").strip()
        symbol = currency_map.get(currency_name)
        if symbol:
            return symbol
        else:
            print("Currency name not found. Please try again.")

def fetch_exchange_rate(currency):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.exchangerate-api.com/v4/latest/{currency}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data_json = json.dumps(data)
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        
        if not redis_client.exists(currency):
            redis_client.setex(currency, 3600, data_json)
            print("Exchange rate data has been fetched and stored in Redis.")
        else:
            redis_client.setex(currency, 3600, data_json)
            print("Exchange rate data is already up to date.")
    else:
        print("Failed to fetch exchange rate data from API")

def get_exchange_rate(currency):
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    
    if redis_client.exists(currency):
        data_json = redis_client.get(currency)
        return json.loads(data_json)
    else:
        return None

def display_exchange_rate(currency):
    exchange_data = get_exchange_rate(currency)
    if exchange_data:
        exchange_rate = exchange_data['rates']
        print("Exchange rates (1", currency, "):")
        for key, value in exchange_rate.items():
            print(key, ":", value)
    else:
        print("No exchange rate data available for the specified currency.")

if __name__ == "__main__":
    currency = get_currency_from_user()
    fetch_exchange_rate(currency)
    display_exchange_rate(currency)
