import random


# базовый класс героя
class Hero:
    def __init__(self, name, hp, power, crit, dodge):
        # основные характеристики героя
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.power = power
        self.crit = crit
        self.dodge = dodge

        # слоты экипировки (меч и броня)
        self.equipment = {"weapon": None, "armor": None}

        # пассивные способности героя
        self.passives = []

        # кулдауны способностей
        self.cooldowns = {}

        # временные характеристики на один раунд боя
        self.temp_power = self.power
        self.temp_crit = self.crit
        self.temp_dodge = self.dodge
        self.temp_defense = 0


    def reset_cooldowns(self):
        # сбрасываем все кулдауны
        for key in self.cooldowns:
            self.cooldowns[key] = 0


    def is_alive(self):
        # проверяем жив ли герой
        return self.hp > 0


    def base_power(self):
        # урон с учетом оружия
        power = self.power
        weapon = self.equipment.get("weapon")
        if weapon:
            power += weapon.power
        return power


    def total_defense(self):
        # защита с учетом брони
        defense = getattr(self, "defense", 0)
        armor = self.equipment.get("armor")
        if armor:
            defense += armor.defense
        return defense


    def total_crit(self):
        # шанс крита с учетом оружия
        crit = self.crit
        weapon = self.equipment.get("weapon")
        if weapon:
            crit += weapon.crit
        return crit


    def total_dodge(self):
        # шанс уклонения с учетом брони
        dodge = self.dodge
        armor = self.equipment.get("armor")
        if armor:
            dodge += armor.dodge
        return dodge


    def crit_hit(self):
        # проверяем выпал ли критический удар
        chance = self.temp_crit
        return random.randint(1, 100) <= chance


    def dodge_hit(self):
        # проверяем уклонился ли герой
        chance = self.temp_dodge
        return random.randint(1, 100) <= chance

class Knight(Hero):
    def __init__(self):
        # создаём рыцаря с повышенным hp и защитой
        super().__init__("Рыцарь", 250, 23, 10, 5)
        self.cooldowns["defense"] = 0
        self.passives = ["iron_skin", "counter_attack"]


    def ability(self, game):
        # кулдаун способности
        if self.cooldowns.get("defense", 0) > 0:
            print("⏳ способность недоступна.")
            return False

        # даём эффект полной защиты
        game.effects.append({"type": "invincible", "turns": 3})
        self.cooldowns["defense"] = 3
        print("+++++++Рыцарь активировал полную защиту!+++++++")
        return True

class Archer(Hero):
    def __init__(self):
        # создаём лучника с высоким критом и уклонением
        super().__init__("Лучник", 170, 27, 30, 25)
        self.cooldowns["snipe"] = 0
        self.passives = ["evasion", "bleed_arrows"]


    def ability(self, game):
        # кулдаун способности
        if self.cooldowns.get("snipe", 0) > 0:
            print("⏳ способность недоступна.")
            return False

        # даём гарантированный крит
        game.effects.append({"type": "guaranteed_crit", "turns": 2})
        self.cooldowns["snipe"] = 2
        print("+++++++Смертельный выстрел активен!+++++++")
        return True

class Mage(Hero):
    def __init__(self):
        # создаём мага с высоким уроном
        super().__init__("Маг", 140, 30, 20, 10)
        self.cooldowns["fire"] = 0
        self.passives = ["arcane_power", "mana_burn"]


    def ability(self, game):
        # кулдаун способности
        if self.cooldowns.get("fire", 0) > 0:
            print("⏳ способность недоступна.")
            return False

        # добавляем эффект горения врагу
        game.effects.append({"type": "burn", "damage": 10, "turns": 2})
        self.cooldowns["fire"] = 2
        print("🔥 огненный взрыв активен!")
        return True