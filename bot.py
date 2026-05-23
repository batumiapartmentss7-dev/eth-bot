import requests

TELEGRAM_TOKEN = "8857597899:AAGALX8vOUNl_sNQyOazFdjrPHBJ8QAzQDs"
CHAT_ID = "1152105552"

SYMBOLS = ["ETHUSDT", "BTCUSDT"]  # добавьте нужные пары

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_symbol(symbol):
    urls = [
        f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=7",
        f"https://api1.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=7",
        f"https://api2.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=7",
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
        send_telegram(f"❌ {symbol}: не удалось получить данные с Binance")
        return

    closed = klines[:-1]  # все закрытые свечи
    last_5 = closed[-5:]  # последние 5

    all_red = all(float(k[4]) < float(k[1]) for k in last_5)

    info = []
    for k in last_5:
        color = "🔴" if float(k[4]) < float(k[1]) else "🟢"
        info.append(color)
    candles_str = " ".join(info)

    if all_red:
        send_telegram(f"🚨 {symbol}: 5 красных свечей подряд!\n{candles_str}")
        print(f"Сигнал отправлен: {symbol}")
    else:
        print(f"{symbol}: сигнала нет — {candles_str}")

# Запуск
for symbol in SYMBOLS:
    check_symbol(symbol)
