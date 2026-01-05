import random
from items import *
def apply_effects(hero, game):
    # применяет все эффекты зелий и способностей на текущий раунд боя
    # сброс временных характеристик на базовые + экипировка
    hero.temp_power = hero.base_power()
    hero.temp_crit = hero.total_crit()
    hero.temp_dodge = hero.total_dodge()
    hero.temp_defense = hero.total_defense()

    # применяем эффекты зелий и способностей
    for eff in game.effects[:]:
        if eff["type"] == "strength":
            hero.temp_power += eff["value"]
        elif eff["type"] == "weakness":
            hero.temp_power -= eff["value"]
        elif eff["type"] == "crit_up":
            hero.temp_crit += eff["value"]
        elif eff["type"] == "dodge_up":
            hero.temp_dodge += eff["value"]
        elif eff["type"] == "shield":
            hero.passives.append("shield")
            hero.shield_value = eff["value"]
        elif eff["type"] == "guaranteed_crit":
            hero.temp_crit = 100  # гарантированный крит
        elif eff["type"] == "burn":
            pass  # наносится врагу в бою
        elif eff['type'] == 'invincible':
            pass

    # уменьшаем длительность эффектов
    for eff in game.effects[:]:
        eff["turns"] -= 1
        if eff["turns"] <= 0:
            game.effects.remove(eff)
            if eff["type"] == "shield" and hasattr(hero, "shield_value"):
                del hero.shield_value
            if eff["type"] == "guaranteed_crit":
                hero.temp_crit = hero.total_crit()

def battle(game, enemy):
    hero = game.hero
    print(f"\n⚔️ {hero.name} vs {enemy.name}")
    hero.reset_cooldowns()

    while hero.is_alive() and enemy.is_alive():
        apply_effects(hero, game)  # обновляем характеристики с эффектами

        print(f"\nHP героя: {hero.hp} | HP врага: {enemy.hp}")
        print("1. Атака")
        print("2. Зелье")
        print("3. Способность")
        print("4. Инвентарь")
        print("5. Сохранить и выйти")

        c = input("> ")

        if c == "2":
            pots = [i for i in game.inventory if isinstance(i, Potion)]
            if not pots:
                print("Зелий нет.")
                continue
            pots[0].use(game)
            game.inventory.remove(pots[0])
            continue

        elif c == "3":
            hero.ability(game)
            continue

        elif c == "4":
            game.open_inventory()
            continue

        elif c == "5":
            game.save()
            print("Игра сохранена. Выход...")
            exit()

        # Атака героя
        dmg = hero.temp_power
        if hero.crit_hit():
            dmg = int(dmg * 1.5)
            print("💥 КРИТ!")
        enemy.hp -= dmg
        print(f"Вы нанесли {dmg} урона.")

        # Эффекты на врага
        for eff in game.effects[:]:
            if eff["type"] == "poison":
                enemy.hp -= eff["damage"]
                print("☠️ Яд наносит урон.")
            if eff["type"] == "bleed":
                bleed = int(enemy.hp * eff["percent"])
                enemy.hp -= bleed
                print(f"🩸 Кровоточит: {bleed}")
            if eff["type"] == "burn":
                enemy.hp -= eff["damage"]
                print("🔥 Горение. Противник обгорает и теряет 10 единиц здоровья")

            eff["turns"] -= 1
            if eff["turns"] <= 0:
                game.effects.remove(eff)

        # атака врага
        if enemy.is_alive():
            dmg = enemy.choose_action(hero)

            # проверка на неуязвимость (эффект рыцаря)
            invincible = next((e for e in game.effects if e.get("type") == "invincible"), None)
            if invincible:
                dmg = 0
                print(" Рыцарь полностью поглощает урон!")

            # проверка уклонения героя
            elif hero.dodge_hit():
                dmg = 0
                print(" Герой уклонился!")

            else:
                # урон броне
                armor = hero.equipment.get("armor")
                if armor and armor.slot == "armor" and armor.durability > 0:
                    absorbed = min(dmg, armor.durability)
                    armor.durability -= absorbed
                    dmg -= absorbed
                    print(f"🛡 Броня {armor.name} поглотила {absorbed} урона! (Остаток прочности: {armor.durability})")
                    if armor.durability <= 0:
                        print(f"️ Броня {armor.name} сломалась!")
                        hero.equipment["armor"] = None

                # урон по герою
                if dmg > 0:
                    hero.hp -= dmg
                    print(f"{enemy.name} наносит {dmg} урона герою.")

    # после боя
    if hero.is_alive():
        print(f"******* Победа над {enemy.name} *******")
        drop_loot(game)
        return True
    else:
        death_menu(game)
        return False

def death_menu(game):
    #менюшка смерти
    while True:
        print("\n~~~~~~~ Вы погибли. ~~~~~~~")
        print("1. Начать заново")
        print("2. Загрузить последнее сохранение")
        print("3. Выйти из игры")

        choice = input("> ")

        if choice == "1":
            # сброс игры
            game.reset()
            from main import main
            main()
            break

        elif choice == "2":
            if game.load():
                # возврат к последней локации
                from locations import resume_location
                resume_location(game)
            else:
                print(" Сохранений нет.")
                game.reset()
                from main import main
                main()
            break

        elif choice == "3":
            print("👋 Выход из игры...")
            exit()

        else:
            print(" Неверный выбор, попробуйте снова.")
