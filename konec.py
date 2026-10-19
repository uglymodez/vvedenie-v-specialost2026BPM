import random

SIZE = 5  # размер поля SIZE x SIZE
MAX_ITEMS = 4  # вместимость инвентаря


field = []
for i in range(SIZE):
    row = []
    for j in range(SIZE):
        row.append(random.choice(["пусто", "пусто", "монстр", "сундук", "банька"]))
    field.append(row)
mapa = []
for j in range(SIZE):
    fow = []
    for k in range(SIZE):
        fow.append('?')
    mapa.append(fow)

field[0][0] = "пусто"  # стартовая клетка безопасна
field[SIZE - 1][SIZE - 1] = "выход"  # противоположный угол

player = {
    "hp": 100,
    "x": 0,  # строка
    "y": 0,  # столбец
    "inventory": [],  # список предметов (строки)
    "bonus": 0,  # прибавка к урону (зачарованный меч / зелье силы)
    "armor": 0,  # защита (зачарованный щит)
}

ITEMS = ["зелье лечения", "зелье силы", "зачарованный меч", "зачарованный щит", "какашка", "барматуха"]


def show_inventory():
    print("Инвентарь:", player["inventory"], f"({len(player['inventory'])}/{MAX_ITEMS})")


def use_item():

    if not player["inventory"]:
        print("Инвентарь пуст.")
        return
    for number, item in enumerate(player["inventory"], 1):
        print(number, "-", item)
    choice = input("Номер предмета (Enter - отмена): ")
    if not choice.isdigit() or not 1 <= int(choice) <= len(player["inventory"]):
        return
    item = player["inventory"].pop(int(choice) - 1)

    if item == "зелье лечения":
        player["hp"] = min(100, player["hp"] + 30)
        print("Вы вылечились на 30. HP:", player["hp"])
    elif item == "зелье силы":
        player["bonus"] += 3
        print("Ваш урон навсегда +3!")
    elif item == "зачарованный меч":
        player["bonus"] += 5
        print("Меч светится! Урон +5.")
    elif item == "зачарованный щит":
        player["armor"] += 3
        print("Щит светится! Защита +3.")
    elif item == "какашка":
        print("Вы швырнули какашкой в монстра, его здоровье уменьшилось на 1")
        return "какашка"
    elif item == "барматуха":
        player["armor"] += 5
        player["bonus"] += 5
        print("Расколбас! Защита + 5, Урон + 5")


def open_chest():
    print("Вы нашли сундук!\n"
          "Открыть - 1, Идти дальше - 2:")
    item = random.choice(ITEMS)
    if len(player["inventory"]) >= MAX_ITEMS:
        print("Но инвентарь полон, нужно выложить один из предметов или идти дальше")
        y = input("Go - идти дальше, Take - выложить предмет и взять новый")
        if y == "Go":
            return
        else:
            vibor = input("Выберите предмет, который хотите заменить\n"
                          "1 - Первый\n"
                          "2 - Второй\n"
                          "3 - Третий\n"
                          "4 - Четвертый\n")
            if vibor == "1":
                player["inventory"][0] = item
            elif vibor == "2":
                player["inventory"][1] = item
            elif vibor == "3":
                player["inventory"][2] = item
            elif vibor == "4":
                player["inventory"][3] = item

    f = input()
    if f != "1" and f != "2":
        print("Неизвестная команда\n"
              "Ошибка, выберите один из вариантов (1 или 2)")
        return open_chest()
    elif f == "1":
        print(f"Поздравляем вы нашли {item}! Хотите взять его с собой или нет:\n"
              f"1 - да, 2 - нет")
        while True:
            t = input()
            if t == "1":
                player["inventory"].append(item)
                print("Вы получили:", item)
                show_inventory()
                return
            elif t == "2":
                return
            else:
                print("Неизвестная команда\n"
                      "Ошибка, выберите один из вариантов (1 или 2)")

    elif f == "2":
        return

def fight():
    monster_hp = random.randint(20, 40)
    print("На вас напал монстр! HP монстра:", monster_hp)

    while monster_hp > 0 and player["hp"] > 0:
        print(f"\nВаше HP: {player['hp']}, HP монстра: {monster_hp}")
        action = input("1 - атаковать, 2 - использовать предмет, 3 - попробовать убежать: ")

        if action == "1":
            damage = random.randint(8, 15) + player["bonus"]
            monster_hp -= damage
            print("Вы ударили монстра на", damage)
        elif action == "2":
            result = use_item()
            if result == "какашка":
                monster_hp -= 1
            else:
                use_item()

        elif action == "3":
            uspeh = random.randint(1, 10)
            if uspeh <= 2:
                print("Вы успешно убежали, Поздравляем!!")
                return
            elif uspeh > 2:
                damage = random.randint(8, 15) - player["armor"]
                print(f"При попытке убежать монстер поймал вас и снёс вам {damage}HP")
        else:
            print("Неверная команда.")
            continue

        if monster_hp > 0:
            damage = random.randint(5, 12) - player["armor"]
            if damage < 1:
                damage = 1
            player["hp"] -= damage
            print("Монстр ударил вас на", damage)

    if player["hp"] <= 0:
        return False
    print("Вы победили монстра!")
    return True

def banka():
    print("Поздравляем! Можете расслабиться, вы попали в баньку, здесь у вас есть возможность попариться и восстановить своё здоровье")
    deistv = input ("1 - пойти в хаммам, 2 - пойти в русскую баньку, 3 - выйти: ")
    if deistv == "1":
        i = random.randint(1, 10)
        player["hp"] += i
        print(f"Ваше здоровье увеличиось на{i}")
        return
    if deistv == "2":
        i = random.randint(1, 10)
        player["hp"] += i
        print(f"Ваше здоровье увеличилось на {i}")
        return
    if deistv == "3":
        return
print("Вы в лабиринте. Дойдите до клетки выхода (правый нижний угол).")
print("w - вверх, s - вниз, a - влево, d - вправо, i - инвентарь, q - выход, m - открыть карту лабиринта")


posItion_X = 0
posItion_Y = 0
while True:
    print(f"\nВы в клетке ({player['x']}, {player['y']}), HP: {player['hp']}")
    command = input("Что делать? ")

    if command == "q":
        print("Вы вышли из игры.")
        break
    elif command == "i":
        show_inventory()
        use_item()
        continue
    new_x = player["x"]
    new_y = player["y"]
    if command == "m":
        mapa[posItion_X][posItion_Y] = '*'
        for fow in mapa:
            print(fow)
        print("* - Вы тут")
        print("? - Неизвестные комнаты лабиринта")
        print("C - В этой комнате сундук")
        print("M - В этой комнате был монстр, сейчас она пустая")
        print("Б - В этой комнате банька, сейчас она пустая")
    elif command == "w":
        new_x -= 1
        posItion_X = new_x
    elif command == "s":
        new_x += 1
        posItion_X = new_x
    elif command == "a":
        new_y -= 1
        posItion_Y = new_y
    elif command == "d":
        new_y += 1
        posItion_Y = new_y
    else:
        print("Неизвестная команда.")
        continue

    # проверка границ поля
    if new_x < 0 or new_x >= SIZE or new_y < 0 or new_y >= SIZE:
        print("Там стена!")
        continue

    player["x"] = new_x
    player["y"] = new_y
    cell = field[new_x][new_y]

    if cell == "монстр":
        if not fight():
            print("Вы погибли... Игра окончена.")
            break
        field[new_x][new_y] = "пусто"# монстр побеждён
        mapa[new_x][new_y] = 'М'
    elif cell == "сундук":
        open_chest()
        field[new_x][new_y] = "пусто"  # сундук уже пуст
        mapa[new_x][new_y] = "С"

    elif cell == "банька":
        banka()
        field[new_x][new_y] = "пусто"
        mapa[new_x][new_y] = "Б"

    elif cell == "выход":
        print("Поздравляем! Вы нашли выход и победили!")
        break
    else:
        print("Пустая комната.")