import asyncio
import websockets
import json
import gzip
import io
from schema import TradeType
from backtesting import log_open_position,log_closed_position,update_position


URL = "wss://open-api-swap.bingx.com/swap-market" 
# WebSocket tracking function to track real-time price of a coin pair
async def track_price(coin_pair: str,type:TradeType, buy_range: tuple, targets: list, stop_loss: float):
    """
    Track price of the given coin pair and check against the given targets and stop loss.
    """
    has_bought = False
    new_sl_value = None
    position_closed = False
    signal_id = None
    price = 0
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

        while not position_closed:
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
                    
                    if data:
                        price = float(data['p'])
                    sl =  stop_loss
                    print(f"Current Price for {coin_pair}-USDT: {price}")

                    # ── LONG LOGIC ─────────────────────────────────────────────────────────────
                    if type == TradeType.LONG:
                        
                        if not has_bought and price>buy_range[0] and price<buy_range[1]:
                            # Place the order here (interaction with broker API)
                            print(f"buying the ETH bcz price {price}is between {buy_range[0]} and {buy_range[1]}")
                            # Log open position and get signal ID when order is placed
                            signal_id = log_open_position(coin_pair, type.name, price)
                            # entry_price = bingXbuy_maretPrice()
                            has_bought = True
                            new_sl_value = round(price*1.005 ,2) # replace it with entry_price 

                        if has_bought:
                            for i, target in enumerate(targets, 1):
                                if price >= target and new_sl_value:
                                    print(f"Target {i} reached for {coin_pair}. Updating SL to: {new_sl_value}")
                                    update_position(signal_id, target_reached=f"TP{i}", stop_loss_triggered=None, new_sl_value=new_sl_value)
                                    break

                            if price >= targets[-1]:
                                print(f"All targets hit for {coin_pair}. Exiting position.")
                                log_closed_position(signal_id, price, target_reached="TP4", stop_loss_triggered=None)
                                position_closed = True
                                break

                            if price <= stop_loss:
                                print(f"Stop Loss hit for {coin_pair} at price {price}. Closing the position.")
                                log_closed_position(signal_id, price, target_reached=None, stop_loss_triggered="Yes")
                                position_closed = True
                                break
                    
                    # ── SHORT LOGIC ─────────────────────────────────────────────────────────────
                    elif type == TradeType.SHORT:
                        if not has_bought and price > buy_range[0] and price < buy_range[1]:
                            signal_id = log_open_position(coin_pair, type.name, price)
                            # entry_price = bingXbuy_maretPrice()
                            has_bought = True
                            new_sl_value = round(price * 0.995, 2) # replace it with entry_price

                        if has_bought:
                            for i, target in enumerate(targets, 1):
                                if price <= target and new_sl_value:
                                    print(f"Target {i} reached for {coin_pair}. Updating SL to: {new_sl_value}")
                                    update_position(signal_id, target_reached=f"TP{i}", stop_loss_triggered=None, new_sl_value=new_sl_value)
                                    break

                            # Close the position if TP4 or Stop Loss is hit
                            if price <= targets[-1]:
                                print(f"All targets hit for {coin_pair}. Exiting position.")
                                log_closed_position(signal_id, price, target_reached="TP4", stop_loss_triggered=None)
                                position_closed = True
                                break

                            if price >= stop_loss:
                                print(f"Stop Loss hit for {coin_pair} at price {price}. Closing the position.")
                                log_closed_position(signal_id, price, target_reached=None, stop_loss_triggered="Yes")
                                position_closed = True
                                break

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