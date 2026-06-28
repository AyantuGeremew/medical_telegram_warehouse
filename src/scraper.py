from telethon.sync import TelegramClient
from datetime import datetime

from config import API_ID, API_HASH, PHONE, SESSION_NAME
from logger import get_logger
from storage import save_json
from downloader import save_image

logger = get_logger()

# -----------------------------------
# Channels (you can extend this list)
# -----------------------------------
CHANNELS = [
    "CheMed",
    "LobeliaCosmetics",
    "TikvahPharma",
    "Thequorachannel",
    "MedInEthio",
    "Debol_Che"
    # Add more from et.tgstat.com/medicine
]


# -----------------------------------
# Extract message data
# -----------------------------------
def extract_message_data(message, channel_name, client):
    return {
        "message_id": message.id,
        "date": str(message.date),
        "text": message.message,
        "views": message.views,
        "forwards": message.forwards,
        "media_type": str(type(message.media).__name__) if message.media else None,
        "image_path": save_image(client, message, channel_name)
    }


# -----------------------------------
# Scrape single channel
# -----------------------------------
def scrape_channel(client, channel_name, limit=200):
    logger.info(f"Scraping channel: {channel_name}")

    try:
        entity = client.get_entity(channel_name)

        messages_data = []

        for message in client.iter_messages(entity, limit=limit):
            data = extract_message_data(message, channel_name, client)
            messages_data.append(data)

        file_path = save_json(messages_data, channel_name)

        logger.info(f"Saved data for {channel_name} -> {file_path}")

    except Exception as e:
        logger.error(f"Error scraping {channel_name}: {str(e)}")


def main():
    logger.info("Starting Telegram Scraper...")

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    client.start(phone=PHONE)

    logger.info("Logged in successfully")

    for channel in CHANNELS:
        scrape_channel(client, channel)

    client.disconnect()

    logger.info("Scraping completed")


if __name__ == "__main__":
    main()