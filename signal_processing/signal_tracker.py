import threading
from price_tracking.websocket_tracker import track_price

# Function to track each signal in its own thread
async def track_signal(coin_pair: str, target1: str, target2: str, target3: str, stop_loss: str):
    # Each signal will run in a separate thread
    signal_thread = threading.Thread(
        target=track_price,
        args=(coin_pair, target1, target2, target3, stop_loss)
    )
    signal_thread.start()
