import websockets
import asyncio
import json

# WebSocket tracking function to track real-time price of a coin pair
async def track_price(coin_pair: str, buy_range: tuple, target1: str, target2: str, target3: str, target4: str, stop_loss: str):
    """
    Track price of the given coin pair and check against the given targets and stop loss.
    """
    # Connect to WebSocket
    url = f"wss://open-api-swap.bingx.com/swap-market"  # Replace with your WebSocket URL
    async with websockets.connect(url) as websocket:
        # Subscribe to the market ticker for the coin pair
        subscription_msg = {
            "id": "24dd0e35-56a4-4f7a-af8a-394c7060909c",
            "reqType": "sub",
            "dataType": f"{coin_pair}-USDT@markPrice"
        }
        await websocket.send(json.dumps(subscription_msg))
        print(f"Subscribed to {coin_pair} market price updates")

        while True:
            # Receive price data from WebSocket
            price_data = await websocket.recv()
            try:
                data = json.loads(price_data)
                current_price = float(data['data']['p'])  # Assuming price is in 'data.p'

                print(f"Current Price for {coin_pair}: {current_price}")
                
                # Check if th
                if current_price >= float(target1):
                    print(f"Target 1 reached for {coin_pair}: {current_price}")
                    break
                elif current_price >= float(target2):
                    print(f"Target 2 reached for {coin_pair}: {current_price}")
                    break
                elif current_price >= float(target3):
                    print(f"Target 3 reached for {coin_pair}: {current_price}")
                    break
                elif current_price >= float(target4):
                    print(f"Target 4 reached for {coin_pair}: {current_price}")
                    break
                elif current_price <= float(stop_loss):
                    print(f"Stop Loss hit for {coin_pair}: {current_price}")
                    break
                
            except json.JSONDecodeError as e:
                print(f"Error decoding WebSocket message: {e}")
                pass
            await asyncio.sleep(1)  # Delay for 1 second before checking again


async def process_all_messages():
    # Example to track multiple coin pairs
    # Modify these values based on the signals you process
    await track_price("RVN-USDT", (0.01575, 0.01619), 0.01655, 0.01700, 0.01770, 0.01850, 0.01550)
    # await track_price("XRP-USDT", (0.50, 0.52), 0.55, 0.60, 0.65, 0.70, 0.45)

if __name__ == '__main__':
    asyncio.run(process_all_messages())
