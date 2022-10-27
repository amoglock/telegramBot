import json

from main import Message

a = {"1": "breakfast", "2": "first_course", "3": "entree", "4": "salad"}


async def parse_answer(message: Message) -> str:
    """
    Splits a string into a key and a value and passes them to the add_t_m function. Otherwise, returns an exception
    """

    try:
        key, value = message.text.split(maxsplit=1)
        return await add_to_menu(a[key], value)
    except (KeyError, ValueError):
        return "Неправильно! Число и блюдо.\nНапример\n**4 чай**"


async def add_to_menu(category: str, dish: str) -> str:
    """Adding new element into menu.json"""

    with open('menu.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    if dish.capitalize() in data[category].keys():
        return "Это уже есть в базе"
    data[category][dish.capitalize()] = {"today": False, "photo": None}

    with open('menu.json', 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    return f"Ты успешно добавил {dish.capitalize()} в базу.\nМожно продолжать или введи 'выход'"


# async def set_today():
#     with open('menu.json', 'r', encoding='utf8') as file:
#         data = json.load(file)
#     for value in a.values():
#         for key in data[value]:
#             print(key)
