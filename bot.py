from binance.client import Client
import requests

SYMBOL = "ETHUSDT"
INTERVAL = Client.KLINE_INTERVAL_15MINUTE
TELEGRAM_TOKEN = "8857597899:AAGALX8vOUNl_sNQyOazFdjrPHBJ8QAzQDs"
CHAT_ID = "1152105552"

client = Client()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

klines = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=7)

closed = klines[:-1]
last_5 = closed[-5:]
candle_before = closed[-6]

red = 0
for k in last_5:
    if float(k[4]) < float(k[1]):
        red += 1

before_was_green = float(candle_before[4]) >= float(candle_before[1])

if red == 5 and before_was_green:
    send_telegram("🔴 ETH 15m: завершились 5 красных свечей подряд!")
    print("Уведомление отправлено")
else:
    print(f"Красных свечей: {red}")