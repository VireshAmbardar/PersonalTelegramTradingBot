import asyncio
import websockets
import json
import gzip
import io

URL = "wss://open-api-swap.bingx.com/swap-market" 



# WebSocket tracking function to track real-time price of a coin pair
async def track_price(coin_pair: str, buy_range: tuple, target1: str, target2: str, target3: str, target4: str, stop_loss: str):
    """
    Track price of the given coin pair and check against the given targets and stop loss.
    """
    # Connect to WebSocket
    async with websockets.connect(URL) as websocket:
        # Send subscription message
        subscription_msg = {
            "id": "24dd0e35-56a4-4f7a-af8a-394c7060909c",
            "reqType": "sub",
            "dataType": f"{coin_pair}-USDT@markPrice"
        }

        await websocket.send(json.dumps(subscription_msg))
        print(f"Subscribed to {coin_pair}-USDT market price updates")

        while True:
            # Receive price data from WebSocket
            message = await websocket.recv()
            # Handle decompression
            compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode='rb')
            decompressed_data = compressed_data.read()
            utf8_data = decompressed_data.decode('utf-8')

            
            if utf8_data:
                try:
                    
                    data = json.loads(utf8_data)
                    data  = data['data']
                    price = 0
                    if data:
                        price = data['p']
                    
                    print(f"Current Price for {coin_pair}-USDT: {price}")
                    
                    



                # Check if the current price hits one of the targets or stop loss
                # if current_price >= float(target1):
                #     print(f"Target 1 reached for {coin_pair}: {current_price}")
                #     break
                # elif current_price >= float(target2):
                #     print(f"Target 2 reached for {coin_pair}: {current_price}")
                #     break
                # elif current_price >= float(target3):
                #     print(f"Target 3 reached for {coin_pair}: {current_price}")
                #     break
                # elif current_price >= float(target4):
                #     print(f"Target 4 reached for {coin_pair}: {current_price}")
                #     break
                # elif current_price <= float(stop_loss):
                #     print(f"Stop Loss hit for {coin_pair}: {current_price}")
                #     break

                except json.JSONDecodeError as e:
                    # print(f"Error decoding WebSocket message: {e}")
                    pass

            await asyncio.sleep(1)  # Delay for 1 second before checking again

# Function to handle multiple coin pairs in parallel
async def process_all_messages():
    # Example to track multiple coin pairs
    await track_price("ETH", (0.01575, 0.01619), 0.01655, 0.01700, 0.01770, 0.01850, 0.01550)
    # You can add other coin pairs as needed
    # await track_price("XRP-USDT", (0.50, 0.52), 0.55, 0.60, 0.65, 0.70, 0.45)

# Main entry point for the program
if __name__ == '__main__':
    asyncio.run(process_all_messages())
