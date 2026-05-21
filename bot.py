import requests

SYMBOL = "ETHUSDT"
INTERVAL = "15m"
TELEGRAM_TOKEN = "8857597899:AAGALX8vOUNl_sNQyOazFdjrPHBJ8QAzQDs"
CHAT_ID = "1152105552"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

urls = [
    f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=7",
    f"https://api1.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=7",
    f"https://api2.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit=7",
]

klines = None
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, list):
            klines = data
            break
    except Exception as e:
        print(f"Ошибка: {e}")

if klines is None:
    print("Ne udalos poluchit dannye s Binance")
    exit()

closed = klines[:-1]
last_5 = closed[-5:]

red = 0
for k in last_5:
    if float(k[4]) < float(k[1]):
        red += 1

print(f"Krasnych svechey: {red}")

if red == 5:
    send_telegram("ETH 15m: 5 krasnych svechey podryad!")
    print("Uvedomlenie otpravleno")
