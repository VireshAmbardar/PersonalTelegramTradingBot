import websockets
import asyncio

# Example WebSocket tracking function (adjust based on broker's WebSocket API)
async def track_price(coin_pair: str, target1: str, target2: str, target3: str, stop_loss: str):
    async with websockets.connect('wss://yourbroker.com/price_feed') as websocket:
        while True:
            # Send a message to the WebSocket server to get the current price of the coin pair
            #TODO : Add logic to subscribe to market ticker data.
            await websocket.send(f"GET_PRICE {coin_pair}")
            
            # Receive the price data
            price_data = await websocket.recv()
            current_price = float(price_data)  # Assuming the price is sent as a float

            # Check if the price hits one of the targets or stop loss
            if current_price >= float(target1):
                print(f"Target 1 reached for {coin_pair}: {current_price}")
                break
            elif current_price >= float(target2):
                print(f"Target 2 reached for {coin_pair}: {current_price}")
                break
            elif current_price >= float(target3):
                print(f"Target 3 reached for {coin_pair}: {current_price}")
                break
            elif current_price <= float(stop_loss):
                print(f"Stop Loss hit for {coin_pair}: {current_price}")
                break
            await asyncio.sleep(1)  # Delay for 1 second before checking again


async def process_all_messages():
    
    await track_price("BAT/USDT", 0.1597,0.1577,0.1555,0.1742)

if __name__ == '__main__':
    asyncio.run(process_all_messages())