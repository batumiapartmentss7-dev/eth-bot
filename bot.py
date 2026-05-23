import requests

TELEGRAM_TOKEN = "8857597899:AAGALX8vOUNl_sNQyOazFdjrPHBJ8QAzQDs"
CHAT_ID = "1152105552"

SYMBOLS = ["ETHUSDT"]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_klines(symbol):
    urls = [
        f"https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval=15m&limit=7",
        f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=7",
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"✅ {symbol}: данные получены")
                return data
        except Exception as e:
            print(f"Ошибка {url}: {e}")
    return None

def check_symbol(symbol):
    klines = get_klines(symbol)
    if klines is None:
        send_telegram(f"❌ {symbol}: не удалось получить данные")
        return

    closed = klines[:-1]   # убираем текущую незакрытую свечу
    last_5 = closed[-5:]   # строго последние 5 закрытых

    info = []
    for k in last_5:
        color = "🔴" if float(k[4]) < float(k[1]) else "🟢"
        info.append(color)
    candles_str = " ".join(info)

    print(f"{symbol}: {candles_str}")

    # Все 5 последних закрытых свечей красные?
    all_red = all(float(k[4]) < float(k[1]) for k in last_5)

    if all_red:
        send_telegram(f"🚨 ETHUSDT: 5 красных свечей по 15 минут!\n{candles_str}")

for symbol in SYMBOLS:
    check_symbol(symbol)
