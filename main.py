import json

from pyrogram import Client, filters

import constants

app = Client("my_bot")


@app.on_message(filters.command("location"))
async def send_location(client, message):
    user = message.chat.id
    username = message.chat.first_name
    await app.send_venue(user, latitude=constants.LATITUDE, longitude=constants.LONGITUDE,
                         title=f"{username} You can find us here", address=constants.ADDRESS)


@app.on_message(filters.command("about"))
async def send_location(client, message):
    await app.send_message(message.chat.id, constants.description_about)
    await app.send_photo(message.chat.id, "photo/photo_2022-10-23_14-34-56.jpg",
                         caption=" До встречи за нашим семейным столом!🤗")


@app.on_message(filters.command("menu") | (filters.regex(r"[М-м]еню") & filters.regex(r"[С-с]егодня")))
async def menu_today(client, message):
    await app.send_message(message.chat.id, "Сегодня готовим:\n"
                                            "- Карифурава (крем суп из цветной капусты, с хрустящей курой) 🍜\n"
                                            "- Салат с тыквой, кус-кусом и брынзой 🥗\n"
                                            "- Глазированный свиной бок с булгуром 🥩\n")


@app.on_message(filters.command("add"))
async def add_to_menu(client, message):
    await app.send_message(message.chat.id, "Ты добавляешь новое блюдо в базу.\nЧтобы все прошло успешно, введи "
                                            "сообщение в формате:\n"
                                            "[1, 2, 3 или 4][пробел][название] без скобок.\nГде 1 это завтрак, "
                                            "2 обед, 3 салат, 4 напиток")

    @app.on_message(filters.text)
    async def answer(client_1, new_message):
        try:
            match new_message.text.split(maxsplit=1):
                case ["1", *obj]:
                    await add_new("breakfast", *obj)
                case ["2", *obj]:
                    await add_new("lunch", *obj)
                case ["3", *obj]:
                    await add_new("drinks", *obj)
                case _:
                    await app.send_message(message.chat.id, "Неправильно! Число и блюдо.\nНапример\n**4 чай**")
                    return
            await app.send_message(message.chat.id, "Success")
        except TypeError:
            await app.send_message(message.chat.id, "Ты забыл название через пробел.")


async def add_new(category, dish):
    with open('menu.json', 'r', encoding='utf8') as file:
        data = json.load(file)
        data[0][category].append(dish.capitalize())
        with open('menu.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)


@app.on_message(filters.audio & filters.private)
async def audio(client, message):
    print(message.audio.file_id)


@app.on_message(filters.command("audio"))
async def send_audio(client, message):
    await app.send_audio(message.chat.id, "CQACAgIAAxkBAAIC_WNW4_zF1BgdpaUBUBbwKp_0KmowAAKNJAACPQABuUrQfivkbKM0iB4E")


app.run()
