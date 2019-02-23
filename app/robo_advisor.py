#robo_advisor.py https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/projects/robo-advisor.md

from dotenv import load_dotenv
import json
import os
import requests
import csv
import datetime

#get secret API key
load_dotenv()
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

#user input and validation, guidance from https://github.com/hiepnguyen034

while True:
    symbol = input("Please specify a stock symbol: ") 
    if symbol.isalpha() and len(symbol) <= 5: 
        break
    else:
        print("This does not appear to be a stock ticker. Please ensure you enter a properly-formatted symbol like MSFT with no numbers.")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"  

response = requests.get(request_url)

parsed_response = json.loads(response.text)

#guidance from https://github.com/prof-rossetti
tsd = parsed_response["Time Series (Daily)"]
day_keys = tsd.keys() 
days = list(day_keys) 

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

#formatting keys
t = datetime.datetime.now()

def to_usd(my_price):
    return f"${my_price:,.2f}"

# guidance provided by Prof Rossetti: https://www.youtube.com/watch?v=UXAVOP1oCog&feature=youtu.be
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

#print informational outputs
print("-----------------")
print("STOCK SYMBOL:", symbol)
print("-----------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + str(t.hour) + ":" + str(t.minute) + " on " + str(t.strftime("%B")) + " " + str(t.day) + "," + str(t.year)) #https://github.com/hiepnguyen034
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}")
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_price_usd))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-----------------")

#stock recommendation calculations
if float(latest_price_usd) >= (recent_high-(0.1*recent_high)):
    print("RECOMMENDATION: Buy!")
    print("RECOMMENDATION REASON: Because the latest closing price is greater than ten percent below the recent high price, buying now presents an opportunity to capitalize on the stock's momentum.")
else:
    print("RECOMMENDATION: Don't buy!")
    print("RECOMMENDATION REASON: Because the latest closing price is less than ten percent below the recent high price, don't buy since the stock price is trending downwards.")
print("-----------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-----------------")
print("HAPPY INVESTING!")
print("-----------------")






