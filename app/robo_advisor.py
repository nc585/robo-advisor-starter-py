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

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN&apikey={api_key}"  

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

#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

# TODO: further revise the example outputs below to reflect real information
t = datetime.datetime.now()
def to_usd(my_price):
    return f"${my_price:,.2f}"

print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: " + t.strftime("%Y-%m-%d %H:%M:%S"))
print("-----------------")
print("LATEST DAY OF AVAILABLE DATA:", latest_day)
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_price_usd))}")

# TODO: write functions to read data for recent high and low: 
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-----------------")

# TODO: write investment recommendation using if statements below:
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")
