from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

import internal_actions
from constants import About, BotMessages, Today

app = Client("my_bot")
admin = False  # Flag for special functions
set_today = False


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
    await app.send_photo(message.chat.id, About.photo, caption=" До встречи за нашим семейным столом!🤗")


# For the /menu command or mach a regex in a regular chat message
@app.on_message(filters.command("menu") | (filters.regex(r"[М-м]еню") & filters.regex(r"[С-с]егодня")))
async def menu_today(client: Client, message: Message) -> None:
    """Sends the menu for today"""

    await app.send_message(message.chat.id, f"Сегодня готовим:\n- На завтрак {Today.breakfast}\n"
                                            f"- А после 14: 00 будут:\n{Today.first_course}\n"
                                            f"- {Today.entree}\n- А еще {Today.salad}")


@app.on_message(filters.command("add"))  # For the /add command
async def switch_on(client: Client, message: Message) -> None:
    """Switch the 'admin' to True and following message from user will be processed by 'add_to_menu' func"""

    await admin_switcher()
    bot_message = BotMessages.return_message(message.text)
    await app.send_message(message.chat.id, bot_message)


REPLY_MESSAGE = "Choose the button below"
REPLY_MESSAGE_BUTTONS = [
    [
        "breakfast", "first_course", "entree", "salad"
    ]
]


@app.on_message(filters.command("show_me"))
async def show_buttons(client: Client, message: Message) -> None:
    """Switch set_today flag for set today menu"""

    await set_today_switcher()
    text = BotMessages.return_message(message.text)
    reply_markup = ReplyKeyboardMarkup(REPLY_MESSAGE_BUTTONS, one_time_keyboard=True, resize_keyboard=True)
    await message.reply(
        text=text,
        reply_markup=reply_markup
    )


@app.on_message(
    filters.regex("breakfast") | filters.regex("first_course") | filters.regex("entree") | filters.regex("salad"))
async def show_all(client: Client, message: Message):
    """Actions after pushed button"""

    if set_today:
        data = internal_actions.open_db()
        for a in data[message.text]:
            await app.send_message(message.chat.id, f"{a} {data[message.text][a]['name']}")
        await set_today_switcher()
    else:
        pass


@app.on_message(filters.regex(r"^[С-с]егодня [1-4] \d\d?$"))
async def set_today(client: Client, message: Message):
    """Set menu on today"""
    # TODO: Change names!!!
    _, a, b = message.text.split()
    a = internal_actions.a[a]
    data = internal_actions.open_db()
    b = data[a][b]['name']
    Today.set_today(a, b)


# After the /add command following message will be grab here
@app.on_message(filters.text)
async def switch_off(client: Client, message: Message) -> None:
    """Switcher for 'admin' variable."""

    if admin:
        if message.text == "Выход" or message.text == "выход":
            await admin_switcher()
            await app.send_message(message.chat.id, "Ты вышел из добавления")
            return

        bot_message = await internal_actions.parse_answer(message)
        await app.send_message(message.chat.id, bot_message)


async def admin_switcher() -> None:
    global admin
    if admin:
        admin = False
    else:
        admin = True


async def set_today_switcher() -> None:
    global set_today
    if set_today:
        set_today = False
    else:
        set_today = True


if __name__ == "__main__":
    app.run()
