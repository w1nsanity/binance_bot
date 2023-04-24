from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import requests

bot = AsyncTeleBot('6197417409:AAFlo23nO8aWrdgz7CWYY0YiwxGWbaj4XGI')

@bot.message_handler(commands=['start'])
async def start_message(message):
    app_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    app_markup.add(types.KeyboardButton('Узнать курс 📈'))
    await bot.send_message(message.chat.id, f'Привет {message.chat.first_name}!\n'
                           f'Здесь ты можешь узнать курс P2P на Binance!''', reply_markup=app_markup)
    
    
@bot.message_handler(content_types=["text"])
async def text(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Узнать курс 📈':
            item = get_rates()
            await bot.send_message(message.chat.id, f'{next(item)}'
                                                    f'{next(item)}'
                                                    f'{next(item)}'
                                                    f'{next(item)}'
                                                    f'{next(item)}')
            
            
def get_rates():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.2.810 Yowser/2.5 Safari/537.36'
    }
    
    params = {
        "proMerchantAds": False,
        "page": 1,
        "rows": 10,
        "payTypes": [
          "RosBankNew"
        ],
        "countries": [],
        "publisherType": None,
        "transAmount": "",
        "asset": "USDT",
        "fiat": "RUB",
        "tradeType": "SELL"
    }
    
    response = requests.post(url=url, headers=headers, json=params).json()
    
    for i in range(params['rows']):
        yield f"name: {response['data'][i]['advertiser']['nickName']}\nprice: {response['data'][i]['adv']['price']}\nlimit: {response['data'][i]['adv']['minSingleTransAmount']} - {response['data'][i]['adv']['dynamicMaxSingleTransAmount']} RUB\n\n"
    
    
if __name__ == '__main__':
    asyncio.run(bot.polling())