from model import process_images

import logging
from aiogram import Bot, Dispatcher, executor, types

import os

API_TOKEN = '5226418050:AAGVAgej7jwh97aK-OFLWcpEY1mkG1cNAUY'
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = {}


async def handle_photo(message):
    usr_id = message["from"]["id"]
    style = f'temp/style_{usr_id}.jpg'
    content = f'temp/content_{usr_id}.jpg'
    output = f'temp/output_{usr_id}.png'
    if message['from']['id'] in users:
        await message.photo[-1].download(content)
        await message.reply("Well, processing image now. It could take some time.")
        # do style transform
        process_images(style,
                       content,
                       output)
        await bot.send_photo(message["from"]["id"], types.InputFile(output))
        # clean up
        del users[message['from']['id']]
        os.remove(style)
        os.remove(content)
        os.remove(output)
    else:
        users[message['from']['id']] = True
        await message.photo[-1].download(style)
        await message.reply("Great, now send me picture that will be processed")


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi! Send me picture with style to apply")


@dp.message_handler()
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    print(message)
    await message.reply("Try /help")


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    print(message)
    await handle_photo(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
