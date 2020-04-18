from random import choice
import math
import random
import copy


"""
Входные данные (Рус/EN)
"""

people = [
    "Зеленович",
    "Горчичников",
    "Голубева",
    "Черненко",
    "Краснова",
    "Белов"
]
rooms = [
    "Гостинная",
    "Бильярдная",
    "Консерватория",
    "Столовая",
    "Кухня",
    "Зал",
    "Библиотека",
    "Веранда",
    "Кабинет"
]
weapons = [
    "Подсвечник",
    "Кинжал",
    "Труба",
    "Револьвер",
    "Веревка",
    "Гаечный ключ"
]
#
# people = [
#     "Green",
#     "Mustard",
#     "Peacock",
#     "Plum",
#     "Scarlett",
#     "White"
# ]
# rooms = [
#     "Ballroom",
#     "Billiard Room",
#     "Conservatory",
#     "Dining Room",
#     "Kitchen",
#     "Hall",
#     "Library",
#     "Lounge",
#     "Study"
# ]
# weapons = [
#     "Candlestick",
#     "Dagger",
#     "Pipe",
#     "Revolver",
#     "Rope",
#     "Wrench"
# ]

"""
Запросы
"""


def div_():
    print()
    print("...................................................................")
    print()


def ask_(playing, ask_array):
    print()
    say_(playing, f"Убийцей является персонаж: {ask_array[0]} в помещении: {ask_array[1]} с орудием: {ask_array[2]}?")


def reveal_():
    print()
    print(f"Убийцей был персонаж: {secrets[0]} в помещении: {secrets[1]} с орудием: {secrets[2]}!")


def say_(playing, string):
    print(f"{playing.name}: '" + string + "'")


def deal_():
    """
    Если после раздачи остались карты, выводит их на экран
    """
    if total != []:
        print("Оставшиеся карты: ", total)


def accuse_(playing):
    if playing.accuse != secrets:
        playing.alive = False


def winner_(accuser):
    print()
    if (accuser.alive == True):
        print(accuser.name + " Победил!")
        return True
    else:
        print(accuser.name + " Проиграл!")
        return False


"""
Стратегия игры для человека и бота
"""


def human_(action, query, playing):
    div_()
    # Показывает руку игрока
    print("В руке: ", playing.hand)
    # ask
    if action == "ask":
        a = str(input("Персонаж: "))
        b = str(input("Комната: "))
        c = str(input("Орудие убийства: "))
        ask_(playing, [a, b, c])
        return [a, b, c]
    elif action == "answer":
        return str(input("Совпавшие карты: "))
    else:
        if str(input("Обвинить? ")) == "Да":
            a = str(input("Персонаж: "))
            b = str(input("Комната: "))
            c = str(input("Орудие убийства: "))
            ask_(playing, [a, b, c])
            return [a, b, c]
        else:
            return False


def bot_(action, query, playing):
    div_()
    if action == "ask":
        question = [choice(a) for a in items_bots]
        ask_(playing, question)
        return question
    elif action == "answer":
        intersection = [i for i in query if i in playing.hand]
        if intersection == []:
            return "..."
        else:
            return choice(intersection)
    else:
        print(f"{playing.name} Не бедет объявлять обвинение")

        return False


"""
Игровая логика
"""


def game_():
    """
    Игровая логика, повторяется пока обвиняемый не найден
    """
    p = -1
    accuser = False
    while accuser == False:
        p = (p + 1) % L

        # Пропускаем выбывших
        while (players[p].alive == False):
            p = ((p + 1) % L)

        div_()
        print(f"<< Ходит игрок {players[p].name} >>")

        # Запрос
        guess = players[p].strat("ask", [], players[p])

        # Проверка запроса
        for q in range(L - 1):
            person = (p + q + 1) % L
            response = players[person].strat("answer", guess, players[person])
            say_(players[person], response)
            if response != "...":
                break

        # обвинить?
        players[p].accuse = (players[p].strat("accuse", [], players[p]))

        if (players[p].accuse != False):
            accuse_(players[p])
            accuser = winner_(players[p])


"""
Создание игроков и раздача карт
"""


items = [people, rooms, weapons]
items_bots = copy.deepcopy(items)

def macrornd():
    """
    Принимающая от игроков функция для распределения карт в руку
    :return: массив со списком из 3х карт
    """
    return_array = [rnd(people), rnd(rooms), rnd(weapons)]
    return return_array

def rnd(array):
    """
    Рандомно выбирает элемент из входящего списка
    и удаляет выбраный элемент из дальнейшей выборки
    :return: элемент массива
    """
    choice_element = math.floor(random.random() * len(array) - 1)
    return_element = array[choice_element]
    del array[choice_element]
    return return_element


secrets = macrornd()
while True:
    count_player = int(input("Введите количество игроков (от 3х до 5-ти): "))
    if (count_player < 3 or count_player > 5):
        print(1)
    else:
        break
while True:
    count_humans = int(input("Введите количество людей-игроков: "))
    if (count_humans > count_player or count_humans <= 0):
        print(1)
    else:
        break

c_p = 1
c_h = 1
players = []


class player:
    def __init__(self, number, strat):
        self.name = (f"Игрок {number}")
        self.strat = strat
        self.alive = True
        self.accuse = False
        self.hand = macrornd()


while c_p <= count_player:
    if c_h <= count_humans:
        strat = human_
    else:
        strat = bot_

    players.append(player(c_p, strat))
    c_p += 1
    c_h += 1


L = len(players)
total = []
for u in items:
    for v in u:
        total.append(v)
print()


"""
Старт кода
"""


def main():
    print("--- CLUEDO ---")
    div_()
    deal_()
    game_()
    div_()
    reveal_()


main()



