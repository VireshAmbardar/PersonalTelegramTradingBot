import pandas as pd
import datetime
import uuid

# Initialize an empty DataFrame to track positions
columns = ['Signal ID', 'Coin Pair', 'Trade Type', 'Entry Price', 'Target Reached', 
           'Stop Loss Triggered', 'Exit Price', 'Profit/Loss', 'created_at', 'updated_at']
positions_df = pd.DataFrame(columns=columns)

# Function to log open positions with UUID and time tracking
def log_open_position(signal_id, coin_pair, trade_type, entry_price):
    # Generate a unique Signal ID using UUID  # Create a unique ID for each signal
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #updated_at = created_at  # Initially, created_at and updated_at will be the same
    signal_id = str(uuid.uuid4())
    
    new_position = {
        'Signal ID': signal_id,
        'Coin Pair': coin_pair,
        'Trade Type': trade_type,
        'Entry Price': entry_price,
        'Target Reached': None,
        'Stop Loss Triggered': None,
        'Exit Price': None,
        'Profit/Loss': None,
        'created_at': created_at,
        'updated_at': None
    }
    
    # Append to DataFrame
    global positions_df
    positions_df = positions_df.append(new_position, ignore_index=True)
    return signal_id

# Function to log closed positions
def log_closed_position(signal_id, exit_price, target_reached=None, stop_loss_triggered=None):
    updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Find the open position based on signal_id
    position = positions_df[positions_df['Signal ID'] == signal_id].iloc[0]
    entry_price = position['Entry Price']
    profit_loss = exit_price - entry_price  # Simple profit/loss calculation
    
    # Update the position in the DataFrame
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'Exit Price'] = exit_price
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'Profit/Loss'] = profit_loss
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'Target Reached'] = target_reached
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'Stop Loss Triggered'] = stop_loss_triggered
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'updated_at'] = updated_at

# Function to update positions (for cases where TP2, TP3, SL scenarios happen)
def update_position(signal_id, target_reached, stop_loss_triggered, new_sl_value=None):
    updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Find the open position based on signal_id
    position = positions_df[positions_df['Signal ID'] == signal_id].iloc[0]
    entry_price = position['Entry Price']
    
    if new_sl_value:
        # Update the stop loss if a new value is provided
        positions_df.loc[positions_df['Signal ID'] == signal_id, 'Stop Loss Triggered'] = f"Moved to {new_sl_value}"
    
    # Update the Target Reached status and SL triggered
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'Target Reached'] = target_reached
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'Stop Loss Triggered'] = stop_loss_triggered
    positions_df.loc[positions_df['Signal ID'] == signal_id, 'updated_at'] = updated_at


# Save DataFrame to CSV
def save_to_csv():
    positions_df.to_csv('positions_log.csv', index=False)

# Save DataFrame to Excel (optional)
def save_to_excel():
    with pd.ExcelWriter('positions_log.xlsx', engine='xlsxwriter') as writer:
        positions_df.to_excel(writer, index=False)

# Example Usage:
# log_open_position(coin_pair="ETH-USDT", trade_type="LONG", entry_price=3300)
# log_open_position(coin_pair="BTC-USDT", trade_type="SHORT", entry_price=45000)

# log_closed_position(signal_id=positions_df['Signal ID'][0], exit_price=3400, target_reached="TP1", stop_loss_triggered=None)
# log_closed_position(signal_id=positions_df['Signal ID'][1], exit_price=44000, target_reached="TP2", stop_loss_triggered=None)

# # Save to file
# save_to_csv()
# save_to_excel()

print("Positions have been logged and saved to CSV/Excel.")
