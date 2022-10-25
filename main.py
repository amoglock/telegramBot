import json

from pyrogram import Client, filters
from pyrogram.types import Message

import constants

app = Client("my_bot")
admin = False  # Flag for special functions

# TODO: Move all service functions into another file


@app.on_message(filters.command("location"))  # For the /location command
async def send_location(client: Client, message: Message) -> None:
    """Sends location to user. It uses coordinates from constants.py"""

    user = message.chat.id
    username = message.chat.first_name
    # send_venue() sends not only  an image of the location, but also additionally
    # Name and address parameters for a clearer message.
    await app.send_venue(user, latitude=constants.LATITUDE, longitude=constants.LONGITUDE,
                         title=f"{username} You can find us here", address=constants.ADDRESS)


@app.on_message(filters.command("about"))  # For the /about command
async def send_location(client: Client, message: Message) -> None:
    """Sends description "about" company from constants.py"""

    # Send a message "about" followed by an image in the next message
    await app.send_message(message.chat.id, constants.description_about)
    await app.send_photo(message.chat.id,
                         "AgACAgIAAxkBAAIHCWNYCKw--ZSj3L2IqOcgC8CYUwzBAAK1wzEb563BSgH3lCVfHCF0AAgBAAMCAAN4AAceBA",
                         caption=" До встречи за нашим семейным столом!🤗")


# For the /menu command or mach a regex in a regular chat message
@app.on_message(filters.command("menu") | (filters.regex(r"[М-м]еню") & filters.regex(r"[С-с]егодня")))
async def menu_today(client: Client, message: Message) -> None:
    """Sends the menu for today"""

    await app.send_message(message.chat.id, "Сегодня готовим:\n"
                                            "- Карифурава (крем суп из цветной капусты, с хрустящей курой) 🍜\n"
                                            "- Салат с тыквой, кус-кусом и брынзой 🥗\n"
                                            "- Глазированный свиной бок с булгуром 🥩\n")


@app.on_message(filters.command("add"))  # For the /add command
async def add_to_menu(client: Client, message: Message) -> None:
    """Switch the 'admin' to True and following message from user will be processed by 'add_to_menu' func"""

    global admin
    admin = True
    await app.send_message(message.chat.id, "Ты добавляешь новое блюдо в базу.\nЧтобы все прошло успешно, введи "
                                            "сообщение в формате:\n"
                                            "[1, 2, 3 или 4][пробел][название] без скобок.\nГде 1 это завтрак, "
                                            "2 обед, 3 салат, 4 напиток")


# After the /add command following message will be grab here
@app.on_message(filters.text)
async def answer(client: Client, message: Message) -> None:
    global admin
    # TODO: replace the match case with a more convenient implementation (in an array)

    while admin is True:
        match message.text.split(maxsplit=1):
            case ["1", *obj]:
                await add_new("breakfast", *obj)
            case ["2", *obj]:
                await add_new("lunch", *obj)
            case ["3", *obj]:
                await add_new("salad", *obj)
            case ["4", *obj]:
                await add_new("drinks", *obj)
            case ["Выход" | "выход"]:
                admin = False
                await app.send_message(message.chat.id, "Ты вышел из добавления")
                return
            case _:
                await app.send_message(message.chat.id, "Неправильно! Число и блюдо.\nНапример\n**4 чай**")
                break
        await app.send_message(message.chat.id, "Success")
        break


async def add_new(category: str, dish: str) -> None:
    """Adding new element into menu.json"""

    with open('menu.json', 'r', encoding='utf8') as file:
        data = json.load(file)
        data[0][category].append(dish.capitalize())
        with open('menu.json', 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)


app.run()
