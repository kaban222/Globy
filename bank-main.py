import datetime
import json
import ssl
import threading
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

from flask import Flask, render_template, request, jsonify
from threading import Thread
from flask_cors import CORS

app = Flask('app')
CORS(app)


bot = Bot("6661637402:AAHOn3AWvGSOzbRPbYAvxGD8uS3orjDKfWs", parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot)

BD = {}

#                   #база данных

link="https://viridian-bird-spring.glitch.me"

def load():
    global BD
    try:
        f1 = open("persons.json", "r")
        BD = json.load(f1)
        f1.close()
    except:
        pass

def save():
    global BD
    f1 = open("persons.json", "w")
    json.dump(BD, f1, ensure_ascii=False)
    f1.close()

async def new_pers(chat_id,kkk, msg):
    if kkk not in BD.keys():
        BD[kkk] = {"balance":0,
                   "date":str(str(datetime.datetime.now()).split(".")[0]),
                   "timer":"0",
                   "boost1":1,
                   "boost2":1,
                   "name": msg.from_user.first_name
                   }
        save()
        mention = "<a href='tg://user?id=" + kkk + "'>" + BD[kkk]['name'] + "</>"
        await bot.send_message(chat_id, f"{mention}, Вы зарегестрировались! \nКоманда помощи - /help")



#                   #Отклик бота
@dp.message_handler(commands=["help"])
async def start(msg: types.Message):
    user_id = str(msg.from_user.id)
    await new_pers(msg.chat.id, user_id, msg)
    mention = "<a href='tg://user?id=" + user_id + "'>" + BD[user_id]['name'] + "</>"
    await bot.send_message(msg.chat.id, f"{mention}, Помощь по боту \n"
                                        f"/help - вызваная команда помощи\n"
                                        f"/bal - покажет ваш баланс, аналог команды: б, баланс\n"
                                        f"")
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    kkk = str(msg.from_user.id)
    await new_pers(msg.chat.id, kkk, msg)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть", web_app=WebAppInfo(url=link)))
    if msg.chat.type != "private":
        await bot.send_message(msg.chat.id, "Приветствую тебя в игровом кошельке! \n\nЕсли ты небыл зарегестрирован, то зарегестрировался автоматически. Чтобы посмотреть свой баланс и др. напиши мне в личных сообщениях \start")
    else:
        await bot.send_message(msg.chat.id, "Приветствую тебя в игровом кошельке! \n\nЕсли ты небыл зарегестрирован, то зарегестрировался автоматически. Чтобы посмотреть свой баланс и др. нажми на кнопку ниже", reply_markup=markup)

@dp.message_handler(commands=["bal", "ballance"])
async def start(msg: types.Message):
    global BD
    user_id = str(msg.from_user.id)
    await new_pers(msg.chat.id, user_id, msg)

    mention = "<a href='tg://user?id=" + user_id + "'>" + BD[user_id]['name'] + "</>"

    mention = "<a href='tg://user?id=" + user_id + "'>" + BD[user_id]['name'] + "</>"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть", web_app=WebAppInfo(url=link)))

    txt = f"{mention}, ваш баланс: \n" \
          f"\n" \
          f"обесов: {BD[user_id]['balance']}\n" \
          f"\n" \
          f"Для выхода в приложение, напиши мне в личных сообщениях /start или б\n"
    if msg.chat.type != "private":
        await bot.send_message(msg.chat.id, txt)
    else:
        await bot.send_message(msg.chat.id, txt, reply_markup=markup)

@dp.message_handler()
async def sistema(msg: types.Message):
    global BD
    user_id = str(msg.from_user.id)
    await new_pers(msg.chat.id, user_id, msg)

    mention = "<a href='tg://user?id=" + user_id + "'>" + BD[user_id]['name'] + "</>"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть", web_app=WebAppInfo(url=link)))

    if msg.text in ["баланс", "Баланс", "б", "Б"]:
        txt = f"{mention}, ваш баланс: \n" \
              f"\n" \
              f"обесов: {BD[user_id]['balance']}\n" \
              f"\n" \
              f"Для выхода в приложение, напиши мне в личных сообщениях /start или б\n"
        await bot.send_message(msg.chat.id, txt)



@app.route('/load')
def balance_id():
    id = request.args.get('id')
    mon = BD[id]['balance']
    print("{" + f"'bal':{mon}" + "}")
    return jsonify(message=mon)
    #return "{" + f"'bal':{mon}" + "}"

@app.route("/main")
def main_page():
    return render_template("home.html")

def run():
    app.run(host="0.0.0.0", port=8327)


def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    load()
    keep_alive()
    executor.start_polling(dp)