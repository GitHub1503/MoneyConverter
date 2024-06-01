import telebot
from config import keys, TOKEN
from extensions import ConvertionException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты>\
<в какую валюту перевести>\
<колличество переводимой валюты> \n увидеть список всех доступных валют /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def valuese(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное колличество параметров')

        quote, base, amount = values

        total_base = MoneyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        if quote == 'США' or quote == 'канада' or quote == 'гонконг' or quote == 'сингапур' or quote == 'австралия':
            quote = 'доллар ' + quote

        if base == 'США' or base == 'канада' or base == 'гонконг' or base == 'сингапур' or base == 'австралия':
            base = 'доллар ' + base

        text = f'Цена {amount} {quote} равно {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)