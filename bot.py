import requests

SYMBOL = "ETHUSDT"
INTERVAL = "15m"
TELEGRAM_TOKEN = "8857597899:AAGALX8vOUNl_sNQyOazFdjrPHBJ8QAzQDs"
CHAT_ID = "1152105552"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=7"
response = requests.get(url)
klines = response.json()

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
