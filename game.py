from heroes import Knight, Archer, Mage
from save_load import save_game, load_game
from items import *


# основной класс игры
class Game:
    def __init__(self):
        # выбранный герой
        self.hero = None

        # инвентарь игрока
        self.inventory = []

        # экипировка (меч и броня)
        self.equipment = {"weapon": None, "armor": None}

        # активные эффекты (зелья, способности)
        self.effects = []

        # флаги для сюжета и концовок
        self.flags = set()

        # текущая локация
        self.location = None


    def choose_hero(self):
        # менюшка выбора героя
        print("\nвыберите героя:")
        print("1. рыцарь")
        print("2. лучник")
        print("3. маг")

        while True:
            c = input("> ")
            if c == "1":
                self.hero = Knight()
                break
            elif c == "2":
                self.hero = Archer()
                break
            elif c == "3":
                self.hero = Mage()
                break

        # выводим имя выбранного героя
        print(f"вы выбрали: {self.hero.name}")


    def save(self):
        # сохраняем игру
        save_game(self)


    def load(self):
        # загружаем сохранённую игру
        data = load_game()
        if not data:
            return False

        (
            self.hero,
            self.inventory,
            self.equipment,
            self.effects,
            self.flags,
            self.location
        ) = data

        print("💾 игра загружена.")
        return True


    def open_inventory(self):
        # если инвентарь пуст
        if not self.inventory:
            print("📦 инвентарь пуст.")
            return

        # выводим список предметов
        print("\n📦 инвентарь:")
        for i, item in enumerate(self.inventory, 1):
            if isinstance(item, Equipment):
                print(
                    f"{i}. {item.name} "
                    f"(сила:{item.power} защита:{item.defense} "
                    f"крит:{item.crit} уклонение:{item.dodge})"
                )
            elif isinstance(item, Potion):
                print(f"{i}. {item.name}")
            else:
                print(f"{i}. {item.name}")

        # выбор предмета
        print("выберите номер предмета или 0 для выхода.")
        choice = input("> ")
        if not choice.isdigit() or int(choice) == 0:
            return

        idx = int(choice) - 1
        if idx < 0 or idx >= len(self.inventory):
            print("неверный выбор.")
            return

        item = self.inventory[idx]

        # если экипировка, то надеваем
        if isinstance(item, Equipment):
            equip_item(self, item)
            self.inventory.pop(idx)

        # если зелье, используем
        elif isinstance(item, Potion):
            item.use(self)
            self.inventory.pop(idx)


    def reset(self):
        # полный сброс игры
        if self.hero:
            # восстанавливаем здоровье героя
            self.hero.hp = self.hero.max_hp

            # убираем экипировку
            self.hero.equipment = {"weapon": None, "armor": None}

            # сбрасываем временные характеристики
            self.hero.temp_power = self.hero.power
            self.hero.temp_crit = self.hero.crit
            self.hero.temp_dodge = self.hero.dodge
            self.hero.temp_defense = 0

            # сбрасываем кулдауны
            self.hero.cooldowns = {
                key: 0 for key in getattr(self.hero, "cooldowns", {})
            }

        # очищаем инвентарь и эффекты
        self.inventory = []
        self.effects = []

        # очищаем флаги и локацию
        self.flags = set()
        self.location = None