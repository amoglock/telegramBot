from typing import NamedTuple


# Coordinates and address DOM location, description
class About(NamedTuple):
    latitude = float(41.993007)
    longitude = float(41.763007)
    address = str("67 Ekvtime Takaishvili St, Ureki, Грузия")
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
        if message == "/set_today":
            return BotMessages.set_today_message
    # ===================================================


class Today(NamedTuple):
    breakfast = str()
    first_course = str()
    entree = str()
    salad = str()

    @classmethod
    def set_today(cls):
        pass
# ====================================================
