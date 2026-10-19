#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Консольная игра «Лабиринт»: пройди из клетки (0, 0) в противоположный угол."""

import random
from dataclasses import dataclass
from typing import List, Optional

# ----------------------------- настройки -----------------------------
START_HP = 100
INVENTORY_CAPACITY = 6
DEFAULT_SIZE = 5

# направления: клавиша -> (смещение по строке, смещение по столбцу, название)
DIRS = {
    "w": (-1, 0, "север"),
    "s": (1, 0, "юг"),
    "a": (0, -1, "запад"),
    "d": (0, 1, "восток"),
}
OPPOSITE = {"w": "s", "s": "w", "a": "d", "d": "a"}

WEAPON_ENCHANTS = {
    "огня": "+5 к урону",
    "остроты": "+3 к урону и шанс крита выше",
    "вампиризма": "лечит на 30% нанесённого урона",
}
ARMOR_ENCHANTS = {
    "крепости": "+3 к защите",
    "шипов": "отражает 3 урона атакующему",
}


# ------------------------------ предметы ------------------------------
@dataclass
class Item:
    name: str
    kind: str  # heal | strength | weapon | armor | scroll
    value: int = 0
    enchant: Optional[str] = None

    def title(self) -> str:
        if self.enchant:
            return f"{self.name} {self.enchant}"
        return self.name

    def describe(self) -> str:
        if self.kind == "heal":
            return f"{self.title()} (восстанавливает {self.value} HP)"
        if self.kind == "strength":
            return f"{self.title()} (+{self.value} к урону на 3 боя)"
        if self.kind == "weapon":
            extra = f", {WEAPON_ENCHANTS[self.enchant]}" if self.enchant else ""
            return f"{self.title()} (урон +{self.value}{extra})"
        if self.kind == "armor":
            extra = f", {ARMOR_ENCHANTS[self.enchant]}" if self.enchant else ""
            return f"{self.title()} (защита {self.value}{extra})"
        if self.kind == "scroll":
            return f"{self.title()} (накладывает случайное зачарование на оружие или броню)"
        return self.title()


def random_item() -> Item:
    pool = [
        (Item("Малое зелье лечения", "heal", 30), 25),
        (Item("Большое зелье лечения", "heal", 60), 10),
        (Item("Зелье силы", "strength", 5), 12),
        (Item("Свиток зачарования", "scroll"), 14),
        (Item("Стальной меч", "weapon", 6), 8),
        (Item("Боевой топор", "weapon", 9), 4),
        (Item("Кожаная броня", "armor", 2), 10),
        (Item("Кольчуга", "armor", 4), 7),
        (Item("Латы", "armor", 6), 3),
    ]
    items, weights = zip(*pool)
    chosen = random.choices(items, weights=weights)[0]
    return Item(chosen.name, chosen.kind, chosen.value, chosen.enchant)


# ------------------------------ монстры ------------------------------
@dataclass
class Monster:
    name: str
    hp: int
    dmg_min: int
    dmg_max: int
    boss: bool = False


def make_monster(depth: float) -> Monster:
    """depth от 0 (старт) до 1 (выход): чем дальше, тем сильнее монстры."""
    if depth < 0.3:
        return random.choice([Monster("Крыса", 15, 2, 5), Monster("Летучая мышь", 12, 3, 6)])
    if depth < 0.65:
        return random.choice([Monster("Гоблин", 30, 4, 9), Monster("Скелет", 38, 5, 10)])
    return random.choice([Monster("Тролль", 55, 7, 13), Monster("Тёмный рыцарь", 50, 8, 14)])


# ------------------------------ комната ------------------------------
class Room:
    def __init__(self) -> None:
        self.doors = set()  # клавиши направлений, где есть проход
        self.monster: Optional[Monster] = None
        self.chest = False
        self.floor: List[Item] = []
        self.visited = False


# ------------------------------ игрок ------------------------------
class Player:
    def __init__(self) -> None:
        self.hp = START_HP
        self.max_hp = START_HP
        self.gold = 0
        self.inventory: List[Item] = []
        self.weapon: Optional[Item] = Item("Ржавый кинжал", "weapon", 2)
        self.armor: Optional[Item] = None
        self.buff_fights = 0
        self.buff_value = 0

    def defense(self) -> int:
        if not self.armor:
            return 0
        bonus = 3 if self.armor.enchant == "крепости" else 0
        return self.armor.value + bonus

    def attack_damage(self):
        dmg = random.randint(5, 9)
        crit_chance = 0.10
        if self.weapon:
            dmg += self.weapon.value
            if self.weapon.enchant == "огня":
                dmg += 5
            elif self.weapon.enchant == "остроты":
                dmg += 3
                crit_chance = 0.25
        if self.buff_fights > 0:
            dmg += self.buff_value
        crit = random.random() < crit_chance
        if crit:
            dmg *= 2
        return dmg, crit

    @property
    def alive(self) -> bool:
        return self.hp > 0


# ------------------------------ игра ------------------------------
class Game:
    def __init__(self, size: int) -> None:
        self.size = size
        self.grid: List[List[Room]] = [[Room() for _ in range(size)] for _ in range(size)]
        self.player = Player()
        self.row = 0
        self.col = 0
        self.prev = (0, 0)
        self.generate_maze()
        self.populate()
        self.grid[0][0].visited = True

    # ---- генерация ----
    def generate_maze(self) -> None:
        n = self.size
        seen = [[False] * n for _ in range(n)]
        stack = [(0, 0)]
        seen[0][0] = True
        while stack:
            r, c = stack[-1]
            options = []
            for key, (dr, dc, _) in DIRS.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc]:
                    options.append((key, nr, nc))
            if not options:
                stack.pop()
                continue
            key, nr, nc = random.choice(options)
            self.grid[r][c].doors.add(key)
            self.grid[nr][nc].doors.add(OPPOSITE[key])
            seen[nr][nc] = True
            stack.append((nr, nc))
        # несколько лишних проходов, чтобы лабиринт не был деревом
        for _ in range(max(1, n * n // 5)):
            r, c = random.randrange(n), random.randrange(n)
            key = random.choice(list(DIRS))
            dr, dc, _ = DIRS[key]
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                self.grid[r][c].doors.add(key)
                self.grid[nr][nc].doors.add(OPPOSITE[key])

    def populate(self) -> None:
        n = self.size
        for r in range(n):
            for c in range(n):
                if (r, c) == (0, 0):
                    continue
                room = self.grid[r][c]
                if (r, c) == (n - 1, n - 1):
                    room.monster = Monster("Хранитель лабиринта", 90, 9, 16, boss=True)
                    continue
                roll = random.random()
                if roll < 0.35:
                    depth = (r + c) / (2 * (n - 1))
                    room.monster = make_monster(depth)
                elif roll < 0.60:
                    room.chest = True

    # ---- вывод ----
    def show_map(self) -> None:
        print("\nКарта (P - вы, E - выход, . - посещено, ? - неизвестно):")
        for r in range(self.size):
            line = ""
            for c in range(self.size):
                if (r, c) == (self.row, self.col):
                    line += " P "
                elif (r, c) == (self.size - 1, self.size - 1):
                    line += " E "
                elif self.grid[r][c].visited:
                    line += " . "
                else:
                    line += " ? "
            print(line)

    def status(self) -> str:
        p = self.player
        weapon = p.weapon.title() if p.weapon else "нет"
        armor = p.armor.title() if p.armor else "нет"
        buff = f", бафф силы: {p.buff_fights} боя" if p.buff_fights else ""
        return (f"HP {p.hp}/{p.max_hp} | золото {p.gold} | оружие: {weapon} | "
                f"броня: {armor} (защита {p.defense()}){buff}")

    def describe_room(self) -> None:
        room = self.grid[self.row][self.col]
        print("\n" + "=" * 60)
        print(f"Комната ({self.row}, {self.col}). {self.status()}")
        doors = ", ".join(f"{k} ({DIRS[k][2]})" for k in sorted(room.doors))
        print(f"Проходы: {doors}")
        if room.chest:
            print("Здесь стоит сундук! (o - открыть)")
        if room.floor:
            names = ", ".join(i.title() for i in room.floor)
            print(f"На полу лежит: {names} (g - подобрать)")
        print("Команды: w/a/s/d - идти, i - инвентарь, u - использовать, "
              "x - выбросить, m - карта, h - помощь, q - выход")

    # ---- инвентарь ----
    def give(self, item: Item) -> None:
        p = self.player
        if len(p.inventory) < INVENTORY_CAPACITY:
            p.inventory.append(item)
            print(f"  Вы получили: {item.describe()}")
        else:
            self.grid[self.row][self.col].floor.append(item)
            print(f"  Инвентарь полон! {item.title()} остаётся лежать на полу.")

    def show_inventory(self) -> None:
        p = self.player
        print(f"\nИнвентарь ({len(p.inventory)}/{INVENTORY_CAPACITY}):")
        if not p.inventory:
            print("  пусто")
        for i, item in enumerate(p.inventory, 1):
            print(f"  {i}. {item.describe()}")

    def pick_item(self, prompt: str) -> Optional[Item]:
        self.show_inventory()
        if not self.player.inventory:
            return None
        raw = input(f"{prompt} (номер, Enter - отмена): ").strip()
        if not raw.isdigit():
            return None
        idx = int(raw) - 1
        if 0 <= idx < len(self.player.inventory):
            return self.player.inventory[idx]
        print("Нет такого предмета.")
        return None

    def use_item(self) -> bool:
        """Возвращает True, если предмет был использован."""
        p = self.player
        item = self.pick_item("Что использовать?")
        if item is None:
            return False
        if item.kind == "heal":
            before = p.hp
            p.hp = min(p.max_hp, p.hp + item.value)
            p.inventory.remove(item)
            print(f"  Вы выпили {item.title()}: +{p.hp - before} HP.")
        elif item.kind == "strength":
            p.buff_fights = 3
            p.buff_value = item.value
            p.inventory.remove(item)
            print(f"  Вы чувствуете прилив сил: +{item.value} к урону на 3 боя.")
        elif item.kind == "weapon":
            p.inventory.remove(item)
            if p.weapon:
                p.inventory.append(p.weapon)
            p.weapon = item
            print(f"  Вы взяли в руки: {item.title()}.")
        elif item.kind == "armor":
            p.inventory.remove(item)
            if p.armor:
                p.inventory.append(p.armor)
            p.armor = item
            print(f"  Вы надели: {item.title()}.")
        elif item.kind == "scroll":
            return self.use_scroll(item)
        return True

    def use_scroll(self, scroll: Item) -> bool:
        p = self.player
        print("  На что наложить зачарование? 1 - оружие, 2 - броня")
        choice = input("  > ").strip()
        if choice == "1" and p.weapon:
            p.weapon.enchant = random.choice(list(WEAPON_ENCHANTS))
            p.inventory.remove(scroll)
            print(f"  Оружие засияло! Теперь это {p.weapon.describe()}.")
            return True
        if choice == "2" and p.armor:
            p.armor.enchant = random.choice(list(ARMOR_ENCHANTS))
            p.inventory.remove(scroll)
            print(f"  Броня засияла! Теперь это {p.armor.describe()}.")
            return True
        print("  Нечего зачаровывать (предмет должен быть надет/в руках).")
        return False

    def drop_item(self) -> None:
        item = self.pick_item("Что выбросить?")
        if item:
            self.player.inventory.remove(item)
            self.grid[self.row][self.col].floor.append(item)
            print(f"  Вы выбросили: {item.title()}.")

    def take_from_floor(self) -> None:
        room = self.grid[self.row][self.col]
        if not room.floor:
            print("  На полу ничего нет.")
            return
        for item in list(room.floor):
            if len(self.player.inventory) >= INVENTORY_CAPACITY:
                print("  Инвентарь полон!")
                break
            room.floor.remove(item)
            self.player.inventory.append(item)
            print(f"  Вы подобрали: {item.describe()}")

    def open_chest(self) -> None:
        room = self.grid[self.row][self.col]
        if not room.chest:
            print("  Здесь нет сундука.")
            return
        room.chest = False
        gold = random.randint(10, 50)
        self.player.gold += gold
        print(f"  Вы открыли сундук! Внутри {gold} золота.")
        for _ in range(random.choice([0, 1, 1, 2])):
            self.give(random_item())
        if random.random() < 0.15:
            print("  Из сундука вырывается ловушка! -10 HP.")
            self.player.hp -= 10

    # ---- бой ----
    def fight(self, monster: Monster) -> str:
        """Возвращает 'won', 'fled' или 'dead'."""
        p = self.player
        print(f"\n!!! Вас атакует {monster.name} (HP {monster.hp}, урон {monster.dmg_min}-{monster.dmg_max}) !!!")
        while monster.hp > 0 and p.alive:
            print(f"\n[Вы: {p.hp}/{p.max_hp} HP]  [{monster.name}: {monster.hp} HP]")
            options = "1 - атаковать, 2 - предмет"
            if not monster.boss:
                options += ", 3 - бежать"
            choice = input(f"{options}\n> ").strip()
            if choice == "1":
                dmg, crit = p.attack_damage()
                monster.hp -= dmg
                print(f"  Вы наносите {dmg} урона{' (КРИТ!)' if crit else ''}.")
                if p.weapon and p.weapon.enchant == "вампиризма":
                    heal = max(1, int(dmg * 0.3))
                    p.hp = min(p.max_hp, p.hp + heal)
                    print(f"  Вампиризм: вы восстанавливаете {heal} HP.")
            elif choice == "2":
                if not self.use_item():
                    continue
            elif choice == "3" and not monster.boss:
                if random.random() < 0.5:
                    print("  Вам удалось сбежать!")
                    return "fled"
                print("  Сбежать не удалось!")
            else:
                print("  Неверная команда.")
                continue
            if monster.hp <= 0:
                break
            # ход монстра
            dmg = max(1, random.randint(monster.dmg_min, monster.dmg_max) - p.defense())
            p.hp -= dmg
            print(f"  {monster.name} бьёт вас на {dmg} урона.")
            if p.armor and p.armor.enchant == "шипов":
                monster.hp -= 3
                print("  Шипы брони ранят врага на 3.")
        if not p.alive:
            return "dead"
        if p.buff_fights > 0:
            p.buff_fights -= 1
        print(f"\nВы победили: {monster.name}!")
        gold = random.randint(5, 25) + (50 if monster.boss else 0)
        p.gold += gold
        print(f"  Добыча: {gold} золота.")
        if random.random() < 0.4 and not monster.boss:
            self.give(random_item())
        return "won"

    # ---- перемещение ----
    def move(self, key: str) -> Optional[str]:
        dr, dc, name = DIRS[key]
        self.prev = (self.row, self.col)
        self.row += dr
        self.col += dc
        room = self.grid[self.row][self.col]
        room.visited = True
        print(f"\nВы идёте на {name}...")
        if room.monster:
            result = self.fight(room.monster)
            if result == "dead":
                return "dead"
            if result == "fled":
                self.row, self.col = self.prev
                return None
            boss = room.monster.boss
            room.monster = None
            if boss:
                return "win"
        return None

    # ---- главный цикл ----
    def run(self) -> None:
        print(f"Вы в лабиринте {self.size}x{self.size}. Начало - (0, 0), выход - ({self.size - 1}, {self.size - 1}).")
        print("В конце вас ждёт Хранитель лабиринта. Удачи!")
        while True:
            self.describe_room()
            cmd = input("> ").strip().lower()
            room = self.grid[self.row][self.col]
            result = None
            if cmd in DIRS:
                if cmd in room.doors:
                    result = self.move(cmd)
                else:
                    print("  Там стена.")
            elif cmd == "i":
                self.show_inventory()
            elif cmd == "u":
                self.use_item()
            elif cmd == "x":
                self.drop_item()
            elif cmd == "g":
                self.take_from_floor()
            elif cmd == "o":
                self.open_chest()
            elif cmd == "m":
                self.show_map()
            elif cmd == "h":
                self.show_help()
            elif cmd == "q":
                print("Вы покинули лабиринт.")
                return
            else:
                print("  Неизвестная команда (h - помощь).")
            if not self.player.alive:
                result = "dead"
            if result == "dead":
                print("\nВы погибли в лабиринте... ИГРА ОКОНЧЕНА.")
                print(f"Собрано золота: {self.player.gold}")
                return
            if result == "win":
                print("\n*** ПОЗДРАВЛЯЕМ! Вы победили Хранителя и выбрались из лабиринта! ***")
                print(f"Осталось HP: {self.player.hp}, золота: {self.player.gold}")
                return

    @staticmethod
    def show_help() -> None:
        print("""
Помощь:
  w/a/s/d - идти на север/запад/юг/восток (только через проходы)
  i - инвентарь     u - использовать предмет (зелье, надеть, зачаровать)
  x - выбросить     g - подобрать с пола
  o - открыть сундук   m - карта   q - выход
Зелья лечат, зелье силы усиливает атаку на 3 боя. Свитки накладывают случайные
зачарования на надетое оружие/броню. Инвентарь вмещает ограниченное число вещей.""")


def main() -> None:
    raw = input(f"Размер лабиринта (3-9, Enter = {DEFAULT_SIZE}): ").strip()
    size = int(raw) if raw.isdigit() and 3 <= int(raw) <= 9 else DEFAULT_SIZE
    try:
        Game(size).run()
    except (EOFError, KeyboardInterrupt):
        print("\nИгра прервана.")


if __name__ == "__main__":
    main()


