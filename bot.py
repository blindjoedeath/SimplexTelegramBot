import telebot
import secret
from base import *
from my_types import  *

dialog = {}

bot = telebot.TeleBot(secret.token)

@bot.message_handler(commands=['add_resource'])
def handle_text(message):
    dialog[message.chat.id] = "resource"
    bot.send_message(message.chat.id, "Напиши название ресурса и количество:")

@bot.message_handler(commands=['add_product'])
def handle_text(message):
    dialog[message.chat.id] = "product"
    bot.send_message(message.chat.id, "Напиши название продукта и цену:")

@bot.message_handler(commands=['add_constraint'])
def handle_text(message):
    dialog[message.chat.id] = "constraint"
    resources = ""
    for res in Base.fetch_res_names(message.chat.id):
        resources += res + "\n"
    products = ""
    for prod in Base.fetch_prod_names(message.chat.id):
        products += prod + "\n"

    bot.send_message(message.chat.id, "Твои ресурсы: \n" + resources + "\n\n" +
                                       "Твои продукты: \n" + products)

    bot.send_message(message.chat.id, "Напиши название продукта, ресурса и цену:")



@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        d = dialog[message.chat.id]
        lines = message.text.split('\n')
        if d == "product":
            Base.insert_product(message.chat.id, Product(lines[0], int(lines[1])))
        elif d == "resource":
            Base.insert_resource(message.chat.id, Resource(lines[0], int(lines[1])))
        else:
            Base.insert_constrain(message.chat.id, Constrain(lines[0], lines[1], int(lines[2])))
        bot.send_message(message.chat.id, "Так держать!")

    except ValueError:
        bot.send_message(message.chat.id, "Ты можешь число нормально написать?")
    except sqlite3.Error as e:
        if 'foreign' in e.args:
            bot.send_message(message.chat.id, "Нет такого ресурса/продукта")
        else:
            bot.send_message(message.chat.id, "Такой ресурс уже есть, ало...")
    except:
        bot.send_message(message.chat.id, "Нет так не пойдет, братишка")

bot.polling(none_stop=True,interval=0)
