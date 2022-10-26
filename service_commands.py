import json

from main import Message

a = {"1": "breakfast", "2": "lunch", "3": "salad", "4": "drinks"}


async def parse_answer(message: Message) -> str:
    """
    Splits a string into a key and a value and passes them to the add_t_m function. Otherwise, returns an exception
    """

    try:
        key, value = message.text.split(maxsplit=1)
        await add_to_menu(a[key], value)
        return f"Ты успешно добавил {value} в базу.\nМожно продолжать или введи 'выход'"
    except (KeyError, ValueError):
        return "Неправильно! Число и блюдо.\nНапример\n**4 чай**"


async def add_to_menu(category: str, dish: str) -> None:
    """Adding new element into menu.json"""

    with open('menu.json', 'r', encoding='utf8') as file:
        data = json.load(file)
        data[0][category].append(dish.capitalize())
        with open('menu.json', 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
