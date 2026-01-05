# импорт основного класса игры
from game import Game

# импорт старта
from locations import start_location

# импорт менеджера аккаунтов
from accounts import GameManager


# создаём объект для работы с аккаунтами
game_manager = GameManager()


def login_menu() -> bool:
    # менюшка входа

    print("\n                   ВХОД В ИГРУ")
    print("═" * 50)
    print("\n  1. Войти в существующий аккаунт")
    print("  2. Создать новый аккаунт")
    print("  3. Выход из игры")

    # Бесконечный цикл, пока игрок не выберет правильный вариант
    while True:
        try:
            # Считываем выбор пользователя
            choice = int(input("\n  Выберите: "))

            # Вход в существующий аккаунт
            if choice == 1:
                name = input("\n  Имя пользователя: ").strip()
                if not name:
                    print(" Введите имя!")
                    continue

                password = input("  Пароль: ").strip()

                # логин и пароль
                if game_manager.login(name, password):
                    print(f"\n Добро пожаловать, {name}!")
                    return True
                else:
                    print(" Неверное имя или пароль!")

            # новый аккаунт
            elif choice == 2:
                print("\n СОЗДАНИЕ АККАУНТА")
                name = input("  Имя (латиница, без пробелов): ").strip()
                if not name:
                    print(" Введите имя!")
                    continue

                # существует ли аккаунт
                if game_manager.account_exists(name):
                    print(" Такой аккаунт уже существует!")
                    continue

                password = input("  Пароль (минимум 3 символа): ").strip()
                if len(password) < 3:
                    print(" Пароль слишком короткий!")
                    continue

                password2 = input("  Повторите пароль: ").strip()
                if password != password2:
                    print(" Пароли не совпадают!")
                    continue

                # создаём аккаунт
                if game_manager.create_account(name, password):
                    print(f"\n Аккаунт «{name}» успешно создан!")
                    return True
                else:
                    print(" Ошибка создания аккаунта!")

            elif choice == 3:
                print("\n Выход из игры.")
                return False

            else:
                print(" Выберите 1, 2 или 3")

        # ввод не число
        except ValueError:
            print(" Введите число!")


def main():
    print('\n                                  ===========ПЛАМЯ ИМПЕРИИ==========')
    # если пользователь не вошёл, то выходим
    if not login_menu():
        return

    # создаём игру
    game = Game()

    # менюшка игры
    print("1. Новая игра")
    print("2. Загрузить игру")
    c = input("> ")

    # если выбрали загрузку
    if c == "2":
        if not game.load():
            # если сохранения нет, то создаём героя
            game.choose_hero()
    else:
        # новая игра, выбор героя
        game.choose_hero()

    # первая локация
    start_location(game)


# запуск программы
if __name__ == "__main__":
    main()