from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram Setup
BOT_TOKEN = "8725936806:AAF0EBxVkrzC50MJ1-YhYtydwLgVLWXaaRw"
CHANNEL_ID = "@thepro_binary_alerts"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        
        action = data.get('action', 'UNKNOWN').upper()
        asset = data.get('asset', 'Asset')
        timeframe = data.get('timeframe', '1m')
        
        if action == "BUY" or action == "LONG":
            msg = f"🟢 *BUY (LONG) SIGNAL*\n\n📊 *Asset:* {asset}\n⏱️ *Timeframe:* {timeframe}\n🚀 *Action:* Press HIGHER on Quotex!"
        elif action == "SELL" or action == "SHORT":
            msg = f"🔴 *SELL (SHORT) SIGNAL*\n\n📊 *Asset:* {asset}\n⏱️ *Timeframe:* {timeframe}\n📉 *Action:* Press LOWER on Quotex!"
        else:
            msg = f"⚠️ *Alert:* {action} on {asset}"
            
        send_telegram_message(msg)
        return "Signal Sent", 200
    else:
        return "Invalid Request", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
