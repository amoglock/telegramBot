from pyrogram import Client, filters
from pyrogram.types import Message

import internal_actions
from constants import About, BotMessages

app = Client("my_bot")
admin = False  # Flag for special functions


@app.on_message(filters.command("location"))  # For the /location command
async def send_location(client: Client, message: Message) -> None:
    """Sends location to user. It uses coordinates from constants.py"""

    user = message.chat.id
    username = message.chat.first_name
    # send_venue() sends not only  an image of the location, but also additionally
    # Name and address parameters for a clearer message.
    await app.send_venue(user, latitude=About.latitude, longitude=About.longitude,
                         title=f"{username} You can find us here", address=About.address)


@app.on_message(filters.command("about"))  # For the /about command
async def send_location(client: Client, message: Message) -> None:
    """Sends description "about" company from constants.py"""

    # Send a message "about" followed by an image in the next message
    await app.send_message(message.chat.id, About.description)
    await app.send_photo(message.chat.id,
                         "AgACAgIAAxkBAAIHCWNYCKw--ZSj3L2IqOcgC8CYUwzBAAK1wzEb563BSgH3lCVfHCF0AAgBAAMCAAN4AAceBA",
                         caption=" До встречи за нашим семейным столом!🤗")


# For the /menu command or mach a regex in a regular chat message
@app.on_message(filters.command("menu") | (filters.regex(r"[М-м]еню") & filters.regex(r"[С-с]егодня")))
async def menu_today(client: Client, message: Message) -> None:
    """Sends the menu for today"""

    await internal_actions.set_today()
    await app.send_message(message.chat.id, "Сегодня готовим:\n"
                                            "- Карифурава (крем суп из цветной капусты, с хрустящей курой) 🍜\n"
                                            "- Салат с тыквой, кус-кусом и брынзой 🥗\n"
                                            "- Глазированный свиной бок с булгуром 🥩\n")


@app.on_message(filters.command("add"))  # For the /add command
async def switch_on(client: Client, message: Message) -> None:
    """Switch the 'admin' to True and following message from user will be processed by 'add_to_menu' func"""

    global admin
    admin = True
    await app.send_message(message.chat.id, BotMessages.add_dish_message)


# After the /add command following message will be grab here
@app.on_message(filters.text)
async def switch_off(client: Client, message: Message) -> None:
    """Switcher for 'admin' variable."""

    global admin
    if admin:
        if message.text == "Выход" or message.text == "выход":
            admin = False
            await app.send_message(message.chat.id, "Ты вышел из добавления")
            return
        bot_answer = await internal_actions.parse_answer(message)
        await app.send_message(message.chat.id, bot_answer)

if __name__ == "__main__":
    app.run()
