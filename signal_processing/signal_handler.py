import re
from loguru import logger
import asyncio
from schema import TradeType
# from signal_processing.signal_tracker import track_signal
# Function to process incoming messages and check if they contain a valid buy/sell signal
async def process_signal(message: str):
    # Example regex to extract the signal information (you may need to modify this based on your message format)
    """
    Process the message to extract buy/sell signal details such as coin pair,
    target prices (TP1, TP2, TP3), and stop loss.
    """
    pattern_search = r"""
            \#(\w+\/USDT)                                      # Group 1: Coin pair
            .*?
            (LONG|SHORT|Entry\s*Zone)\s*[:\-]?\s*              # Group 2: Trade type (LONG, SHORT, or Entry Zone)
            ([\d\.]+)\s*[–\-]\s*([\d\.]+)                      # Groups 3-4: Buy range start and end
            .*?
            TP1:\s*([\d\.]+)                                   # Group 5: TP1
            .*?
            TP2:\s*([\d\.]+)                                   # Group 6: TP2
            .*?
            TP3:\s*([\d\.]+)                                   # Group 7: TP3
            .*?
            TP4:\s*([\d\.]+)                                   # Group 8: TP4
            .*?
            STOP\s*LOSS\s*[:\-]?\s*([\d\.]+)                   # Group 9: Stop Loss
        """
    pattern_fallback = r"""
            \#(\w+\/USDT)                              # Group 1: Coin pair
            .*?
            (LONG|SHORT)\s*[:\-]?\s*([\d\.]+)          # Group 2: Trade type, Group 3: Buy start
            .*?
            TP1:\s*([\d\.]+)                           # Group 4: TP1
            .*?
            TP2:\s*([\d\.]+)                           # Group 5: TP2
            .*?
            TP3:\s*([\d\.]+)                           # Group 6: TP3
            .*?
            TP4:\s*([\d\.]+)                           # Group 7: TP4
            .*?
            STOP\s*LOSS\s*[:\-]?\s*([\d\.]+)           # Group 8: Stop Loss
        """

    # Matching the pattern for buy/sell signal
    match = re.search(pattern_search, message,re.DOTALL | re.VERBOSE | re.IGNORECASE)
    fallback = False

    if not match:
        match = re.search(pattern_fallback, message, re.DOTALL | re.VERBOSE | re.IGNORECASE)
        fallback = True


    if match:
        coin_pair = match.group(1)
        trade_type = match.group(2).upper()  # Normalize to "LONG"/"SHORT"
        trade_type = TradeType.SHORT if "SHORT" in trade_type else TradeType.LONG
        
        if not fallback:
            buy_range_start = match.group(3)
            buy_range_end = match.group(4)
            tp1 = match.group(5)
            tp2 = match.group(6)
            tp3 = match.group(7)
            tp4 = match.group(8)
            stop_loss = match.group(9)
        else:
            buy_range_start = match.group(3)
            tp1 = match.group(4)
            buy_range_end = tp1
            tp2 = match.group(5)
            tp3 = match.group(6)
            tp4 = match.group(7)
            stop_loss = match.group(8)
        # logger.info(f"Signal detected: {coin_pair} - Targets: {target1}, {target2}, {target3} - SL: {stop_loss}")
        # print(f"Coin Pair: {coin_pair}, TP1: {target1}, TP2: {target2}, TP3: {target3}, Stop Loss: {stop_loss}")
        print(f"""
            Coin Pair  : {coin_pair},Trade Type : {trade_type}
            Buy Range  : {buy_range_start} - {buy_range_end}
            TP1: {tp1},TP2: {tp2},TP3: {tp3},TP4: {tp4},Stop Loss : {stop_loss}
            """)
                
        # Start tracking the signal in a new thread
        # await track_signal(coin_pair, trade_type, (buy_range_start,buy_range_end), tp1, tp2, tp3, tp4, stop_loss)
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
message4 = """🌺 Pair: #FARTCOIN/USDT 🌺

😎LONG : 1.418

💻Leverage : 25x

Take Profit:

🚀 TP1: 1.4400
🚀 TP2: 1.4800
🚀 TP3: 1.5500
🚀 TP4: 1.6000
🚀 TP5: 1.6600

⛔️ STOP LOSS: 1.2870
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
