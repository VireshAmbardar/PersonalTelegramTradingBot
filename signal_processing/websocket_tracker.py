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
from BingX import generate_listen_key, extend_listen_key

URL = f"wss://open-api-swap.bingx.com/swap-market"

async def track_price(coin_pair: str, type: TradeType, buy_range: tuple, targets: list, stop_loss: float):
    has_bought = False
    new_sl_value = None
    position_closed = False
    signal_id = None
    price = 0

    listining_key = generate_listen_key()

    print(f"Started tracking {coin_pair}-USDT")

    while not position_closed:
        try:
            async with websockets.connect(URL + f"?listenKey={listining_key}") as websocket:
                print(f"Connected to WebSocket for {coin_pair}-USDT")

                subscription_msg = {
                    "id": "24dd0e35-56a4-4f7a-af8a-394c7060909c",
                    "reqType": "sub",
                    "dataType": f"{coin_pair}-USDT@lastPrice"
                }
                await websocket.send(json.dumps(subscription_msg))

                while True:  # not repeating `while not position_closed`
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=60)
                        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode='rb')
                        decompressed_data = compressed_data.read().decode('utf-8')
                        data = json.loads(decompressed_data).get('data')

                        if not data:
                            continue

                        price = float(data['c'])
                        print(f"Price for {coin_pair}-USDT: {price}")

                        if type == TradeType.LONG:
                            if not has_bought and buy_range[0] < price < buy_range[1]:
                                print(f"Buying LONG {coin_pair} at {price}")
                                signal_id = log_open_position(coin_pair, type.name, price)
                                has_bought = True
                                new_sl_value = round(price * 1.005, 2)

                            if has_bought:
                                for i, target in enumerate(targets, 1):
                                    if price >= target:
                                        print(f"LONG Target {i} hit: {target}")
                                        update_position(signal_id, target_reached=f"TP{i}", stop_loss_triggered=None, new_sl_value=new_sl_value)
                                        break

                                if price >= targets[-1]:
                                    log_closed_position(signal_id, price, target_reached="TP4", stop_loss_triggered=None)
                                    print(f"LONG all targets hit. Closing.")
                                    position_closed = True

                                elif price <= stop_loss:
                                    log_closed_position(signal_id, price, target_reached=None, stop_loss_triggered="Yes")
                                    print(f"LONG Stop loss hit. Closing.")
                                    position_closed = True

                        elif type == TradeType.SHORT:
                            if not has_bought and buy_range[0] < price < buy_range[1]:
                                print(f"Buying SHORT {coin_pair} at {price}")
                                signal_id = log_open_position(coin_pair, type.name, price)
                                has_bought = True
                                new_sl_value = round(price * 0.995, 2)

                            if has_bought:
                                for i, target in enumerate(targets, 1):
                                    if price <= target:
                                        print(f"SHORT Target {i} hit: {target}")
                                        update_position(signal_id, target_reached=f"TP{i}", stop_loss_triggered=None, new_sl_value=new_sl_value)
                                        break

                                if price <= targets[-1]:
                                    log_closed_position(signal_id, price, target_reached="TP4", stop_loss_triggered=None)
                                    print(f"SHORT all targets hit. Closing.")
                                    position_closed = True

                                elif price >= stop_loss:
                                    log_closed_position(signal_id, price, target_reached=None, stop_loss_triggered="Yes")
                                    print(f"SHORT Stop loss hit. Closing.")
                                    position_closed = True

                        if position_closed:
                            break  # break out of inner loop, will close websocket

                    except asyncio.TimeoutError:
                        print("Timeout, extending listen key and reconnecting...")
                        extend_listen_key(listining_key)
                        # break  # break to reconnect WebSocket
                        continue

                    except Exception as e:
                        print(f"Error in message loop: {e}")
                        # break  # reconnect on other error
                        continue

        except Exception as e:
            print(f"WebSocket connection error: {e}")
            await asyncio.sleep(3)

    print("Position closed successfully.")

async def process_all_messages():
    await track_price("FARTCOIN", TradeType.LONG, (1.418, 1.4400), [1.4400, 1.4800, 1.5500, 1.6000], 1.2870)

if __name__ == '__main__':
    asyncio.run(process_all_messages())
