import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
import requests

# Load API keys from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# Function to get listenKey (for WebSocket connection)
def get_listen_key():
    url = "https://api.bingx.com/swap/v2/user/stream"
    headers = {
        'API-KEY': API_KEY,
        'API-SECRET': SECRET_KEY
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['data']['listenKey']
    else:
        raise Exception(f"Failed to get listenKey: {response.text}")

# WebSocket URI
BASE_URI = "wss://ws.bingx.com/swap-ws/v2"

# Function to connect to WebSocket and listen for real-time data
async def get_live_data(pair="BTC-USDT"):
    listen_key = get_listen_key()  # Get listenKey for the WebSocket connection
    uri = f"{BASE_URI}?listenKey={listen_key}"
    
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")
        
        # Subscribe to the market data for the pair (BTC/USDT)
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [
                f"market.{pair}.ticker"
            ],
            "id": 1
        }
        
        await websocket.send(json.dumps(subscribe_message))
        
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            
            if "result" in data:
                # Extract the ask price (last trade price) from the response
                ask_price = data['result']['askPrice']
                print(f"Live Ask Price for {pair}: {ask_price}")
            else:
                print("Received data:", data)

# Main entry point to start WebSocket
def main():
    pair = "BTC-USDT"  # You can change this to any other pair like ETH-USDT, etc.
    asyncio.get_event_loop().run_until_complete(get_live_data(pair))

if __name__ == "__main__":
    main()
