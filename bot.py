import requests

TELEGRAM_TOKEN = "8857597899:AAGALX8vOUNl_sNQyOazFdjrPHBJ8QAzQDs"
CHAT_ID = "1152105552"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_symbol(symbol):
    url = f"https://api.bybit.com/v5/market/kline?category=linear&symbol={symbol}&interval=15&limit=7"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        klines = data["result"]["list"]
    except Exception as e:
        print(f"Ошибка {symbol}: {e}")
        send_telegram(f"❌ {symbol}: не удалось получить данные с Bybit")
        return

    # Bybit отдаёт от новых к старым — разворачиваем
    klines = list(reversed(klines))

    closed = klines[:-1]   # убираем текущую незакрытую свечу
    last_5 = closed[-5:]   # последние 5 закрытых свечей

    # Проверяем что ВСЕ 5 подряд красные
    all_red = all(float(k[4]) < float(k[1]) for k in last_5)

    info = []
    for k in last_5:
        color = "🔴" if float(k[4]) < float(k[1]) else "🟢"
        info.append(color)

    candles_str = " ".join(info)
    print(f"{symbol}: {candles_str} | Все красные: {all_red}")

    if all_red:
        send_telegram(f"🚨 {symbol} 15m: 5 красных свечей подряд!\n{candles_str}\nВремя входить в Лонг!")

check_symbol("BTCUSDT")
check_symbol("ETHUSDT")
