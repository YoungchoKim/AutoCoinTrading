import pyupbit
import time

tickers = ["KRW-BTC", "KRW-XRP"]
price = pyupbit.get_current_price(tickers)
print(price)



krw_tickers = pyupbit.get_tickers(fiat="KRW")
price_file = open('price_file_date', 'w')

prices = pyupbit.get_current_price(krw_tickers)
print(prices)

for k,v in prices.items():
    print(k,v)


coin_list = list(prices.keys())
now = time.localtime()
price_file.write("date,")

for coin in coin_list:
    price_file.write(coin + ',')
price_file.write('\n')

while True:
    now = time.localtime()
    price_file.write("%04d-%02d-%02d %02d:%02d:%02d," % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    prices = pyupbit.get_current_price(krw_tickers)
    for coin in coin_list:
        price_file.write(str(prices[coin])+',')
    price_file.write('\n')
    time.sleep(1)

price_file.close()
