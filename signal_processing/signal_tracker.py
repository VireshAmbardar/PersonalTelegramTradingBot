import threading
from concurrent.futures import ThreadPoolExecutor
from price_tracking.websocket_tracker import track_price
from schema import TradeType

MAX_THREADS = 5

semaphore = threading.Semaphore(MAX_THREADS)

executor = ThreadPoolExecutor(max_workers=MAX_THREADS)

# Function to track each signal in its own thread
async def track_signal(coin_pair: str,trade_type:TradeType, buy_range:tuple, target1: str, target2: str, target3: str,target4: str, stop_loss: str):
    # Each signal will run in a separate thread
    
    # signal_thread = threading.Thread(
    #     target=track_price,
    #     args=(coin_pair, target1, target2, target3, stop_loss)
    # )
    # signal_thread.start()
    coin_name  = coin_pair.split('/')[0]
    executor.submit(track_price, coin_name ,buy_range, target1, target2, target3, target4,stop_loss)
