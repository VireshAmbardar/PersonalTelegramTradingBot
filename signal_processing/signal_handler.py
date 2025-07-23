import re
# from signal_processing.signal_tracker import track_signal
# from signal_processing.signal_tracker import track_signal
from loguru import logger
import asyncio
# Function to process incoming messages and check if they contain a valid buy/sell signal
async def process_signal(message: str):
    # Example regex to extract the signal information (you may need to modify this based on your message format)
    """
    Process the message to extract buy/sell signal details such as coin pair,
    target prices (TP1, TP2, TP3), and stop loss.
    """
    # Regex patterns for messages containing valid buy/sell signals
    # print(message)
    pattern_search = r"""
            \#(\w+\/USDT)                 
            .*?                          
            TP1:\s*([\d\.]+)             
            .*?                          
            TP2:\s*([\d\.]+)             
            .*?                          
            TP3:\s*([\d\.]+)             
            .*?                          
            [Ss][Tt][Oo][Pp]\s*[Ll][Oo][Ss][Ss]:?\s*([\d\.]+)  
        """
    # Matching the pattern for buy/sell signal
    match = re.search(pattern_search, message,re.DOTALL | re.VERBOSE | re.IGNORECASE)

    if match:
        coin_pair = match.group(1)  # e.g., "RVN/USDT"
        target1 = float(match.group(2))    # TP1 value
        target2 = float(match.group(3))    # TP2 value
        target3 = float(match.group(4))    # TP3 value
        stop_loss = float(match.group(5))  # Stop Loss value
        
        # logger.info(f"Signal detected: {coin_pair} - Targets: {target1}, {target2}, {target3} - SL: {stop_loss}")
        print(f"Coin Pair: {coin_pair}, TP1: {target1}, TP2: {target2}, TP3: {target3}, Stop Loss: {stop_loss}")
        
        # Start tracking the signal in a new thread
        # await track_signal(coin_pair, target1, target2, target3, stop_loss)
        # print(coin_pair, target1, target2, target3, stop_loss)

# Sample 
message1 = """🌺 Pair: #SOL/USDT 🌺

🎯 Target = {1, 2,} ✅

JOIN VIP COMMUNITY 📺
"""
message2 = """🌺 Pair: #RVN/USDT (LONG) 🌺

Entry Zone: 0.01575 - 0.01619

💻 Leverage: Cross 20x 

Targets:

🚀 TP1: 0.01655
🚀 TP2: 0.01700
🚀 TP3: 0.01770
🚀 TP4: 0.01850
🚀 TP5: 0.02000+

⛔ Stoploss: 0.01550
"""
message3 = """OKX Futures, Binance Futures, KuCoin Futures
#RVN/USDT Entered entry zone ✅
Period: 16 Minutes ⏰
"""
message4 = """Dear members, #RVN is Near to its Target! 🎯

I would really appreciate it if you could share your profit screenshots after hitting target 1. 😇

Don’t forget to share your ROI screenshot 😊❤️

Share👉 @Crypto_Space001 ✅️
"""
message5 = """🌺 Trade: #B***/USDT 🌺

💻 LEVERAGE: Premium 

1🚀 Premium 🔐
2🚀 Premium 🔐

Join Premium Get Access Signals 
CONTACT ViP: ⭐️

JOIN VIP COMMUNITY 📺
"""
message6 = """Binance Futures, Bitget Futures
#RVN/USDT Take-Profit target 1 ✅
Profit: 44.4719% 📈
Period: 5 Hours 14 Minutes ⏰
"""
message7 = """🌺 Pair: #BAT/USDT 🌺

SHORT : 0.1666 – 0.1645

💻 Leverage : 5x – 10x

Take Profit:

🚀 TP1: 0.1597
🚀 TP2: 0.1577
🚀 TP3: 0.1555
🚀 TP4: 0.1523

⛔️ STOP LOSS: 0.1742"""

async def process_all_messages():
    for i in [message1,message2,message3,message4,message5,message6,message7]:
        await process_signal(i)

if __name__ == '__main__':
    asyncio.run(process_all_messages())
