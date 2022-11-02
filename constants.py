from typing import NamedTuple


# Coordinates and address DOM location, description
class About(NamedTuple):
    latitude = float(41.99415)
    longitude = float(41.76485)
    address = str("40 Guria St, Ureki, Грузия")
    photo = str("AgACAgIAAxkBAAIHCWNYCKw--ZSj3L2IqOcgC8CYUwzBAAK1wzEb563BSgH3lCVfHCF0AAgBAAMCAAN4AAceBA")
    description = str("Мы открыли DOM в Грузии!\n""DOM - это не ресторан или кафе, это место, где тебя ждут и дарят "
                      "добро. ""Мы меняем меню каждый день, угощаем если у вас нет денег и даём понять, ""что DOM - "
                      "не точка на карте, а состояние души 🙌\n\n""В течении дня, за очень скромную плату, "
                      "есть возможность попробовать: ""салат, суп, горячее или всё сразу.\n""🥐 Завтрак - 5 лари (до "
                      "14:00)\n🍜 Суп - 10 лари\n🥗 Салат -  5 лари\n""🍝 Горячее - 10 лари\n ☕️ Напитки ( кофе, чай, "
                      "морс ) - 1 лари\n""🍷 Бокал домашнего вина - 5 лари \n\n")
# ==================================================


class BotMessages(NamedTuple):
    add_dish_message = str("Ты добавляешь новое блюдо в базу.\nЧтобы все прошло успешно, введи "
                           "сообщение в формате:\n"
                           "[число от 1 до 5][пробел][название] без скобок.\nГде 1 это завтрак, "
                           "2 первое блюдо, 3 второе блюдо, 4 салат")

    set_today_message = str("Устанавливаем меню на сегодня:")

    @staticmethod
    def return_message(message):
        if message == "/add":
            return BotMessages.add_dish_message
        if message == "/show_me":
            return BotMessages.set_today_message
    # ===================================================


class Today(NamedTuple):
    breakfast = str()
    first_course = str()
    entree = str()
    salad = str()

    @staticmethod
    def set_today(a, dish):
        if a == "breakfast":
            Today.breakfast = dish
        elif a == "first_course":
            Today.first_course = dish
        elif a == "entree":
            Today.entree = dish
        elif a == "salad":
            Today.salad = dish
# ====================================================
