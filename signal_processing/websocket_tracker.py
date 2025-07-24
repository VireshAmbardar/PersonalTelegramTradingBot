import asyncio
import websockets
import json
import gzip
import io
from schema import TradeType


URL = "wss://open-api-swap.bingx.com/swap-market" 
# WebSocket tracking function to track real-time price of a coin pair
async def track_price(coin_pair: str,type:TradeType, buy_range: tuple, target1: float, target2: float, target3: float, target4: float, stop_loss: float):
    """
    Track price of the given coin pair and check against the given targets and stop loss.
    """
    has_bought = False
    new_sl_value = None
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
                        price = float(data['p'])
                    sl =  stop_loss
                    print(f"Current Price for {coin_pair}-USDT: {price}")

                    # ── LONG LOGIC ─────────────────────────────────────────────────────────────
                    if type == TradeType.LONG:
                        if not has_bought and price>buy_range[0] and price<buy_range[1]:
                            # Place the order here (interaction with broker API)
                            print(f"buying the ETH bcz price {price}is between {buy_range[0]} and {buy_range[1]}")
                            
                            has_bought = True
                            new_sl_value = round(price*1.005 ,2)
                            

                        elif has_bought and price>target1 and new_sl_value:
                            print(f"Target 1 reached for {coin_pair}. Updating SL to: {new_sl_value}")
                            sl = new_sl_value
                            # Update the stop loss value to the new SL

                        elif has_bought and price>target2:
                            print("Sell 30% of the position")

                        elif has_bought and price<sl:
                            print("Close the position")

                    # ── SHORT LOGIC ─────────────────────────────────────────────────────────────
                    if type == TradeType.SHORT:
                        if not has_bought and price>buy_range[0] and price<buy_range[1]:
                            print(f"buying the ETH bcz price {price}is between {buy_range[0]} and {buy_range[1]}")

                        elif has_bought and price<target1:
                            print("Sell 30% of the position  and move SL to Entry")
                            # update the SL value

                        elif has_bought and price<target2:
                            print("Sell 30% of the position")

                        elif has_bought and price>sl:
                            print("Close the position")

                except json.JSONDecodeError as e:
                    # print(f"Error decoding WebSocket message: {e}")
                    pass

            await asyncio.sleep(1)  # Delay for 1 second before checking again

# Function to handle multiple coin pairs in parallel
async def process_all_messages():
    # Example to track multiple coin pairs
    await track_price("ETH",TradeType.LONG, (3300.23, 3400), 3756, 4000 , 4500, 5500, 3000)
    # You can add other coin pairs as needed
    # await track_price("XRP-USDT",,"SHORT" (0.50, 0.52), 0.55, 0.60, 0.65, 0.70, 0.45)

# Main entry point for the program
if __name__ == '__main__':
    asyncio.run(process_all_messages())
