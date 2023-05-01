from telegram.ext import *
import csv
from aiogram import Bot, Dispatcher, executor, types
# import pyqrcode

import requests
import time

bot = Bot(token='5886980999:AAGvbq5923XF0dTQDczFjOpfm4oyDnRadb0')
dp = Dispatcher(bot)

print ('Bot started....')
order_details = ''
full_name=''
address=''
phone=''
item=0

def start(update,context):
    update.message.reply_text("Hello there! I\'m food-plug. How may I help you?")
    update.message.reply_text("/Menu")
    update.message.reply_text("/Order")
    update.message.reply_text("/Exit")

def Menu(update,context):
    base_url = "https://api.telegram.org/bot5886980999:AAGvbq5923XF0dTQDczFjOpfm4oyDnRadb0/sendPhoto"

    my_file = open("menu.png", "rb")

    parameters = {
        "chat_id": "5719120623",
        "caption": "Menu"
    }

    files = {
        "photo": my_file
    }

    resp = requests.get(base_url, data=parameters, files=files)
    print(resp.text)

    update.message.reply_text("/Order")
    update.message.reply_text("/Exit")

def help_command(update, context):
    update.message.reply_text('If you need any assistance. I am here to help')

def Order(update,context):
    global item,order_details, full_name, address, phone
    order_details = ''
    full_name = ''
    address = ''
    phone = ''
    item = 0
    update.message.reply_text("Order with complete detail:")


def Exit(update,context):
    update.message.reply_text("Thank you for getting in touch")

def handlmsg(update,context):
    print(update.message.text)
    global item,order_details,full_name,address ,phone

    if item == 0:
        order_details = update.message.text
        update.message.reply_text("Please enter you details:")
        update.message.reply_text("Full_name:")

    if item == 1:
        full_name = update.message.text
        update.message.reply_text("Address:")

    if item == 2:
        address = update.message.text
        update.message.reply_text("Phone Number:")

    if item == 3:
        phone = update.message.text
        update.message.reply_text("Order: "+order_details)
        update.message.reply_text("Full_name: "+full_name)
        update.message.reply_text("Address: "+address)
        update.message.reply_text("Phone: "+phone)
        update.message.reply_text('Is the Order confirmed?')
        print(order_details)
        print(full_name)
        print(address)
        print(phone)
        update.message.reply_text('/Confirm')
        update.message.reply_text('/Cancel')

    item += 1

def Confirm(update,context):
    header = ['Order_details','Full name', 'address', 'Phone']
    data = [order_details,full_name, address, phone]
    with open('record.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(data)
    f.close()
    update.message.reply_text('Thank you for ordering, we will contact you soon')

def Cancel(update, context):
    update.message.reply_text("Cancelled.....")
    update.message.reply_text("/Order")
    update.message.reply_text("/Exit")

def error(update, context):
    print(f'Update {update} caused error{context.error}')


def main():
    updater = Updater("5886980999:AAGvbq5923XF0dTQDczFjOpfm4oyDnRadb0", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('Order', Order))
    dp.add_handler(CommandHandler('Confirm', Confirm))
    dp.add_handler(CommandHandler('Menu', Menu))
    dp.add_handler(CommandHandler('Exit', Exit))
    dp.add_handler(CommandHandler('Cancel', Cancel))
    dp.add_handler(MessageHandler(Filters.text, handlmsg))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
main()
