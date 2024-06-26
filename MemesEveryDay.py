import logging
import random
import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Установите ваш токен бота
TOKEN = '7278409108:AAH07ssap9XCdZapZlJY7SmuidfTpCExDuQ'
# Установите ID вашего канала
CHANNEL_ID = '@memeseverydayss'
# Установите путь к папке с мемами
MEMES_FOLDER = 'I:\\MemesEveryDay'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=TOKEN)

def get_memes_from_folder(folder_path, extensions=['.jpg', '.jpeg', '.png', '.gif']):
    memes = []
    for file in os.listdir(folder_path):
        if any(file.endswith(ext) for ext in extensions):
            memes.append(os.path.join(folder_path, file))
    return memes

async def send_meme():
    memes = get_memes_from_folder(MEMES_FOLDER)
    if not memes:
        logger.warning('No memes found in the folder')
        return
    try:
        meme = random.choice(memes)
        with open(meme, 'rb') as photo:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo)
        logger.info(f'Sent meme: {meme}')
    except TelegramError as e:
        logger.error(f'Failed to send meme: {e}')

async def main():
    # Отправка первого мема сразу после запуска
    await send_meme()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_meme, 'interval', hours=1)
    scheduler.start()
    logger.info('Scheduler started')

    try:
        while True:
            await asyncio.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info('Scheduler shutdown')

if __name__ == '__main__':
    asyncio.run(main())