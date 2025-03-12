from flask import Flask, request
import requests

app = Flask(__name__)

# Replace with your actual Telegram Bot Token
TELEGRAM_BOT_TOKEN = "YOUR_NEW_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "-1002429178256"  # Replace with your chat ID or group ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return {"status": "error", "message": "No data received"}, 400

    # Extract trade details
    trade_type = data.get("type", "Unknown")  # Buy/Sell
    pair = data.get("pair", "Unknown Pair")
    stop_loss = data.get("stop_loss", "N/A")
    take_profits = data.get("take_profits", [])

    # Format message
    message = "\n".join([
        "\U0001F514 Trade Alert \U0001F514",
        f"{trade_type} {pair}",
        *[f"TP{i+1}: {tp}" for i, tp in enumerate(take_profits)],
        f"SL: {stop_loss}"
    ])

    # Send to Telegram
    response = requests.post(TELEGRAM_API_URL, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    })

    return {"status": "success", "message": "Alert sent"}, response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
