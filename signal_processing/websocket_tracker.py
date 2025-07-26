import asyncio
import websockets
import json
import gzip
import io
from schema import TradeType
from backtesting import log_open_position, log_closed_position, update_position

import os
from dotenv import load_dotenv
load_dotenv()
from BingX import generate_listen_key,extend_listen_key

URL = f"wss://open-api-swap.bingx.com/swap-market"

# WebSocket tracking function to track real-time price of a coin pair
async def track_price(coin_pair: str, type: TradeType, buy_range: tuple, targets: list, stop_loss: float):
    """
    Track price of the given coin pair and check against the given targets and stop loss.
    """
    has_bought = False
    new_sl_value = None
    position_closed = False
    signal_id = None
    price = 0

    while not position_closed:
        try:
            # Attempt to connect to WebSocket
            listining_key = generate_listen_key()
            async with websockets.connect(URL + f"?listenKey={listining_key}") as websocket:
                print(f"Subscribed to {coin_pair}-USDT market price updates")

                subscription_msg = {
                    "id": "24dd0e35-56a4-4f7a-af8a-394c7060909c",
                    "reqType": "sub",
                    "dataType": f"{coin_pair}-USDT@markPrice"
                }
                subscription_msg_ = {
                    "id": "24dd0e35-56a4-4f7a-af8a-394c7060909c",
                    "reqType": "sub",
                    "dataType": f"{coin_pair}-USDT@lastPrice"
                }

                await websocket.send(json.dumps(subscription_msg))

                while not position_closed:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=60)
                        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode='rb')
                        decompressed_data = compressed_data.read()
                        utf8_data = decompressed_data.decode('utf-8')

                        if utf8_data:
                            data = json.loads(utf8_data).get('data')
                            if data:
                                price = float(data['p'])
                                print(f"Current Price for {coin_pair}-USDT: {price}")
                                if price<=1.355 or price >= 1.36:
                                    break

                                # ── LONG LOGIC ─────────────────────────────────────────────────────────────
                                if type == TradeType.LONG:
                                    if not has_bought and buy_range[0] < price < buy_range[1]:
                                        print(f"Buying {coin_pair} at {price}, within range {buy_range}")
                                        signal_id = log_open_position(coin_pair, type.name, price)
                                        has_bought = True
                                        new_sl_value = round(price * 1.005, 2)

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

                                        elif price <= stop_loss:
                                            print(f"Stop Loss hit for {coin_pair} at price {price}. Closing the position.")
                                            log_closed_position(signal_id, price, target_reached=None, stop_loss_triggered="Yes")
                                            position_closed = True

                                # ── SHORT LOGIC ─────────────────────────────────────────────────────────────
                                elif type == TradeType.SHORT:
                                    if not has_bought and buy_range[0] < price < buy_range[1]:
                                        print(f"Buying {coin_pair} at {price}, within range {buy_range}")
                                        signal_id = log_open_position(coin_pair, type.name, price)
                                        has_bought = True
                                        new_sl_value = round(price * 0.995, 2)

                                    if has_bought:
                                        for i, target in enumerate(targets, 1):
                                            if price <= target and new_sl_value:
                                                print(f"Target {i} reached for {coin_pair}. Updating SL to: {new_sl_value}")
                                                update_position(signal_id, target_reached=f"TP{i}", stop_loss_triggered=None, new_sl_value=new_sl_value)
                                                break

                                        if price <= targets[-1]:
                                            print(f"All targets hit for {coin_pair}. Exiting position.")
                                            log_closed_position(signal_id, price, target_reached="TP4", stop_loss_triggered=None)
                                            position_closed = True

                                        elif price >= stop_loss:
                                            print(f"Stop Loss hit for {coin_pair} at price {price}. Closing the position.")
                                            log_closed_position(signal_id, price, target_reached=None, stop_loss_triggered="Yes")
                                            position_closed = True

                    except asyncio.TimeoutError:
                        print(f"Timeout reached while waiting for WebSocket message. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                        extend_listen_key(listining_key)
                        continue  # Retry on timeout

                    except Exception as e:
                        print(f"Error processing message: {e}. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                        
                        continue  # Retry on other errors

        # except websockets.exceptions.WebSocketException as e:
        #     print(f"WebSocket connection error: {e}. Retrying in 3 seconds...")
        #     await asyncio.sleep(3)
        #     continue  # Retry on WebSocket connection failure

        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 3 seconds...")
            await asyncio.sleep(3)
            
            continue  # Retry on other errors

    if position_closed:
        print("Position closed successfully")
    else:
        print("WebSocket closed without closing the position.")

# Function to handle multiple coin pairs in parallel
async def process_all_messages():
    # Example to track multiple coin pairs
    await track_price("FARTCOIN", TradeType.LONG, (1.418, 1.4400), [1.4400, 1.4800, 1.5500, 1.6000], 1.2870)

# Main entry point for the program
if __name__ == '__main__':
    asyncio.run(process_all_messages())
