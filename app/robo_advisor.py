#robo_advisor.py

from dotenv import load_dotenv
import json
import os
import requests
import datetime

load_dotenv()

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

symbol = input("Please specify a stock symbol: ") 
#insert more functionality here to pull up a message if incorrect symbol is entered

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"  

response = requests.get(request_url)

parsed_response = json.loads(response.text)

# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...

#guidance from @prof rossetti
tsd = parsed_response["Time Series (Daily)"]
day_keys = tsd.keys() 
days = list(day_keys) 
#print(days[0]) #> today's date prints  
latest_day = days[0] #> '2019-02-19'
latest_price_usd = tsd[latest_day]["4. close"]

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

high_prices = []

for day in days:
    high_price = tsd[day]["2. high"]
    high_prices.append(float(high_price))
recent_high = max(high_prices)

#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

# TODO: further revise the example outputs below to reflect real information
#t = datetime.datetime.now()
def to_usd(my_price):
    return f"${my_price:,.2f}"

print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("-----------------")
print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT: " + t.strftime("%Y-%m-%d %H:%M:%S"))
print("-----------------")
print("LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_price_usd))}")

# TODO: write functions to read data for recent high and low: 
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(latest_price_usd))}")
print("-----------------")

# TODO: write investment recommendation using if statements below:
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")
