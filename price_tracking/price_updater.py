import threading
import time

# Assuming a basic in-memory price tracking, you can enhance it to integrate with a database if needed
class PriceTracker:
    def __init__(self):
        # This will store the current price for each coin pair
        self.prices = {}

    def update_price(self, coin_pair: str, price: float):
        """Update the price of the coin pair"""
        self.prices[coin_pair] = price
        print(f"Price for {coin_pair} updated: {price}")

    def get_price(self, coin_pair: str):
        """Get the current price of a coin pair"""
        return self.prices.get(coin_pair, None)

# Global price tracker instance
price_tracker = PriceTracker()

# Function to periodically check and update the prices
def update_price_periodically(coin_pair: str, price_data_func, target1: float, target2: float, target3: float, stop_loss: float):
    """Update the price at regular intervals and check if any targets or stop loss are reached"""
    while True:
        # Assuming `price_data_func` fetches the latest price data (from a WebSocket or API)
        current_price = price_data_func(coin_pair)
        
        if current_price is not None:
            # Update the price in the global price tracker
            price_tracker.update_price(coin_pair, current_price)
            
            # Check if the price hit any of the targets or stop loss
            if current_price >= target1:
                print(f"Target 1 hit for {coin_pair} at {current_price}")
                break
            elif current_price >= target2:
                print(f"Target 2 hit for {coin_pair} at {current_price}")
                break
            elif current_price >= target3:
                print(f"Target 3 hit for {coin_pair} at {current_price}")
                break
            elif current_price <= stop_loss:
                print(f"Stop Loss hit for {coin_pair} at {current_price}")
                break
        else:
            print(f"No price data available for {coin_pair}")
        
        # Sleep for a short time before checking the price again (e.g., 1 second)
        time.sleep(1)

# This function would be used to simulate fetching the price from WebSocket or any other source
def mock_price_fetcher(coin_pair: str):
    """Mock function to simulate price fetching. Replace with actual WebSocket or API call."""
    # In a real scenario, you will replace this with actual logic to fetch the price from the WebSocket or API
    # For now, we simulate price change randomly
    import random
    return random.uniform(1.0, 10.0)  # Simulating random price between 1 and 10

# Example usage: Update price periodically for a coin pair
def track_price_in_thread(coin_pair: str, target1: float, target2: float, target3: float, stop_loss: float):
    """Function to run price update in a separate thread for each coin pair"""
    price_update_thread = threading.Thread(
        target=update_price_periodically,
        args=(coin_pair, mock_price_fetcher, target1, target2, target3, stop_loss)
    )
    price_update_thread.start()

# Example of starting a price tracking thread for a coin pair
# if __name__ == '__main__':
#     # Simulate tracking price for a coin pair with target and stop loss
#     track_price_in_thread('APT/USDT', 5.0, 6.0, 7.0, 3.0)
#     track_price_in_thread('XRP/USDT', 1.5, 2.0, 2.5, 1.0)
