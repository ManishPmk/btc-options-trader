from fastapi import FastAPI, Request
import httpx
import uvicorn
import os
from datetime import datetime

app = FastAPI()

# === ENV VARS (set securely in Render or .env) ===
DELTA_API_KEY = os.getenv("DELTA_API_KEY")
DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")
DELTA_BASE_URL = "https://api.delta.exchange"

# === TRADE EXECUTION ===
async def place_order(symbol, price):
    headers = {
        "api-key": DELTA_API_KEY,
        "api-secret": DELTA_API_SECRET,
        "Content-Type": "application/json"
    }

    order = {
        "product_id": 1,  # Update to actual BTCUSDT product ID
        "size": 1,
        "side": "buy",
        "order_type": "market",
        "limit_price": None,
        "stop_price": None
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{DELTA_BASE_URL}/v2/orders", headers=headers, json=order)
        return r.status_code, r.json()

# === WEBHOOK ENDPOINT ===
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    price = data.get("price")
    action = data.get("action")

    print(f"[{datetime.utcnow()}] Signal: {symbol} | {action} @ {price}")

    if action == "BUY":
        status, response = await place_order(symbol, price)
        print("Order Status:", status, response)
        return {"status": status, "response": response}

    return {"message": "Received"}

# Run locally (comment out when deploying to Render)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
