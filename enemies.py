import random
# базовый класс врагов
class Enemy:
    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.power = power
        self.rage = False
        self.evasion = 0
        self.critical_boost = 0

    def is_alive(self):
        # жив ли враг
        return self.hp > 0

    def check_rage(self):
        # стратегии боссов в зав-ти от уровня хп
        if self.hp <= self.max_hp * 0.2:
            # Отчаяние
            self.evasion = 20
            self.critical_boost = 15
            self.rage = True
        elif self.hp <= self.max_hp * 0.4:
            # Злость
            self.rage = True
            self.power = int(self.power * 1.2)

    def choose_action(self, hero):
        # выбор действия врага
        self.check_rage()
        if self.rage:
            roll = random.randint(1, 100)
            if roll <= 30:
                # 30% шанс мощного удара
                dmg = int(self.power * 1.5)
                print(f"🔥 {self.name} входит в ярость и наносит мощный удар {dmg}!")
                return dmg
        # обычная атака
        return self.power

    def dodge_hit(self):
        # шанс уклонения, если активирована одна из стратегий
        return random.randint(1, 100) <= self.evasion

    def crit_hit(self):
        # шанс крита
        chance = self.critical_boost
        return random.randint(1, 100) <= chance

# враги
class Bandit(Enemy):
    def __init__(self):
        # у род. класса берем атрибуты экземпляра (с остальными классами врагов также)
        super().__init__("Разбойник", 70, 12)

class Rka(Enemy):
    def __init__(self):
        super().__init__("Ырка", 100, 19)

class Vamp(Enemy):
    def __init__(self):
        super().__init__("Вампир", 130, 25)

class Dragon(Enemy):
    def __init__(self):
        super().__init__("Древний дракон", 260, 35)