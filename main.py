import asyncio
from telethon import TelegramClient, events
import sys
from loguru import logger
from telethon.errors import RPCError, common
from dotenv import load_dotenv
import os
load_dotenv()

# ── CONFIG ─────────────────────────────────────────────────────────────────────
api_id =  os.getenv('APP_ID')                     # your API ID
api_hash = os.getenv('APP_HASH')

LOG_FILENAME = 'telegram.log'

# ── CONFIGURE LOGURU ────────────────────────────────────────────────────────────
logger.remove()                                  # Remove default sink
logger.add(sys.stderr, level="INFO")             # Console output
logger.add(
    LOG_FILENAME,
    rotation="00:00",      # Rotate daily at midnight
    retention="7 days",    # Keep logs for one week
    compression="zip"      # Compress rotated logs
)

# ── TELETHON CLIENT ─────────────────────────────────────────────────────────────
client = TelegramClient('user_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    """
    This handler is called whenever you receive a new message,
    whether in a private chat or any group/channel you're a member of.
    """
    try:
        sender = await event.get_sender()
        logger.info(sender)
        # print(sender)
        # name = sender.username or sender.first_name
        # print(f"New message from {name}: {event.raw_text}")
        logger.info(f"New message {event.raw_text }")
    except common.TypeNotFoundError as e:
        # Known Telethon deserialization glitch—just warn and continue
        logger.warning(f"Ignored unknown TLObject: {e}")
        pass
    except:
        pass

async def main():
    # Start the client (prompts login on first run)
    await client.start()
    # print("Client is running. Listening for new messages...")
    logger.info("✅ Client started and listening for messages...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
