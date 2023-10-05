import asyncio
import logging
import requests
import yaml
from aiogram import Bot, Dispatcher, types, filters, F
from aiogram.filters.command import Command

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)

with open('config.yaml', 'r') as config_file:
    config_data = yaml.safe_load(config_file)

# bot config
bot_config = config_data['bot']
botName = bot_config['botName']
botToken = bot_config['botToken']
adminId = bot_config['adminId']

#metalvis api config
metalvis_config = config_data['metalvis']
headers = {
  'x-api-key': metalvis_config['x-api-key']
}
api_url = metalvis_config['api_url']
GET_GOODS_BY_ID  = "GetGoodsById"
welcome_message = metalvis_config['wellcome_message']


bot = Bot(token=botToken)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Ти мені артикул, я тобі залишки!")
    
@dp.message()
async def echo_message(message: types.Message):
    text = message.text
    await message.reply("Шукаю інфу по айді: " + text)
    print(message.from_user.id,":" , text)
    goods = get_goods_by_id(text)
    if goods == "Wrong request":
        message_text = "No information"
    else:
        message_text = "Ось що є:" + "\n" + goods['Data'][0]['CategoryName'] + "\n" + goods['Data'][0]['Name'] + "\n" + str(goods['Data'][0]['PriceBaseWithTax']) + " грн.\n" + str(goods['Data'][0]['RestsMainWhQuantity']) + " шт."
    await message.reply(message_text)
    
def isId(text):
    try:
        int(text)
        return True
    except ValueError:
        return False    

def get_goods_by_id(id):
    if not isId(id):
        return "Wrong request"

    payload = [id]
    url = api_url + GET_GOODS_BY_ID
    logging.info("Payload: " + payload.__str__() )
    logging.info("Url: " + url)

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # The request was successful
        data = response.json()
        logging.info(data)
        return data
    else:
        logging.error(f"Request failed with status code {response.status_code}")   
        return "Wrong request" 

async def sendWellcomeMessage():
    try:
        logging.info("Sending [" + welcome_message + "]")
        await bot.send_message(adminId, welcome_message)
    except Exception as e:
        logging.error(f"Error sending welcome message: {str(e)}")
    pass

async def main():
    logging.info("Starting bot")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    logging.info("Starting main loop")
    loop.create_task(main())
    loop.create_task(sendWellcomeMessage())
    loop.run_forever()

