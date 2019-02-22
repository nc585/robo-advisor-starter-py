#robo_advisor.py

from dotenv import load_dotenv
import json
import os
import requests
import csv

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

# guidance provided by Prof Rossetti: https://www.youtube.com/watch?v=UXAVOP1oCog&feature=youtu.be
high_prices = []
low_prices = []

for day in days:
    high_price = tsd[day]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[day]["3. low"]
    low_prices.append(float(low_price))
recent_high = max(high_prices)
recent_low = min(low_prices)

#
# INFO OUTPUTS
#

# TODO: further revise the example outputs below to reflect real information
#t = datetime.datetime.now()
def to_usd(my_price):
    return f"${my_price:,.2f}"

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open (csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for day in days:
        daily_prices = tsd[day]
        writer.writerow({
            "timestamp": day,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"],
    })
    writer.writerow({
        "timestamp": "Todo",
        "open": "Todo",
        "high": "Todo",
        "low": "Todo",
        "close": "Todo",
        "volume": "Todo",
    })    

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
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-----------------")

# TODO: write investment recommendation using if statements below:
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")


# TODO: write response data to a CSV file
print("-----------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-----------------")
print("HAPPY INVESTING!")
print("-----------------")

# guidance provided by Prof Rossetti: https://www.youtube.com/watch?v=UXAVOP1oCog&feature=youtu.be





