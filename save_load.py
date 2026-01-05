import pickle
import os

# папка для сохранений
save_dir = "saves"

# путь к файлу сохранения
save_file = os.path.join(save_dir, "save.pkl")

# если папки для сохранений нет, то создаём её
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


def save_game(game):
    # сохраняем данные игры в файл

    with open(save_file, "wb") as f:
        # сохраняем основные данные игры
        pickle.dump(
            (
                game.hero,        # герой игрока
                game.inventory,   # инвентарь
                game.equipment,   # надетая экипировка
                game.effects,     # эффекты
                game.flags,       # флаги сюжета
                game.location     # текущая локация
            ),
            f
        )

    print("💾 игра сохранена.")


def load_game():
    # загружаем игру

    # если сохранения нет, то выводим сообщение
    if not os.path.exists(save_file):
        print("❌ нет сохранений.")
        return None

    # открываем файл и загружаем данные
    with open(save_file, "rb") as f:
        return pickle.load(f)


def has_save():
    # существует ли файл сохранения
    return os.path.exists(save_file)