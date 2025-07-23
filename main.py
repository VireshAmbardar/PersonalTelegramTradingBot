import asyncio
from telethon import TelegramClient, events
import sys
from loguru import logger
from telethon.errors import common
from dotenv import load_dotenv
import os
from signal_processing.signal_handler import process_signal

load_dotenv()

# ── CONFIG ─────────────────────────────────────────────────────────────────────
api_id = os.getenv('APP_ID')  # your API ID
api_hash = os.getenv('APP_HASH')

LOG_FILENAME = 'telegram.log'

# ── CONFIGURE LOGURU ────────────────────────────────────────────────────────────
logger.remove()  # Remove default sink
logger.add(sys.stderr, level="INFO")  # Console output
logger.add(
    LOG_FILENAME,
    rotation="00:00",  # Rotate daily at midnight
    retention="7 days",  # Keep logs for one week
    compression="zip"  # Compress rotated logs
)

# ── TELETHON CLIENT ─────────────────────────────────────────────────────────────
client = TelegramClient('user_session', api_id, api_hash)

# Channel IDs
Billion_Forex_Channel_id = 1175415497 
Nitro_Channel_id = 1802644203 
Crypt_Space_Channel_id = 1879457222

# ── EVENT CLIENT ─────────────────────────────────────────────────────────────
@client.on(events.NewMessage(chats=[Crypt_Space_Channel_id]))
async def handle_new_message(event):
    try:
        sender = await event.get_sender()
        logger.info(f"New message received: {event.raw_text}")
        
        # Process the message to see if it contains a trading signal
        await process_signal(event.raw_text)

    except common.TypeNotFoundError as e:
        logger.warning(f"Ignored unknown TLObject: {e}")
        pass
    except Exception as e:
        logger.error(f"Error processing message: {e}")

# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
async def main():
    await client.start()
    logger.info("✅ Client started and listening for messages...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
