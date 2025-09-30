import os
import random
import time

# Файл для счётчика участников
COUNTER_FILE = "participants_count.txt"

# 🗂️ ОГРОМНАЯ БАЗА ВОПРОСОВ (30+)
QUESTIONS_DB = [
    # ——————————————— УРОВЕНЬ 1: НОВИЧОК ———————————————
    {"level": 1, "text": "Какой символ используется для комментариев в Python?", "answers": ["#"]},
    {"level": 1, "text": "Как вывести текст на экран в Python?", "answers": ["print"]},
    {"level": 1, "text": "Какой тип данных используется для хранения целого числа?", "answers": ["int"]},
    {"level": 1, "text": "Как создать пустой список?", "answers": ["[]", "list()"]},
    {"level": 1, "text": "Какой оператор используется для сравнения 'равно'?", "answers": ["=="]},

    # ——————————————— УРОВЕНЬ 2: ДЖУН ———————————————
    {"level": 2, "text": "Какой тип данных неизменяемый: list или tuple?", "answers": ["tuple"]},
    {"level": 2, "text": "Как объявить функцию в Python?", "answers": ["def"]},
    {"level": 2, "text": "Что выведет: len('hello')?", "answers": ["5"]},
    {"level": 2, "text": "Как добавить элемент в конец списка?", "answers": ["append"]},
    {"level": 2, "text": "Какой модуль используется для работы с датой и временем?", "answers": ["datetime"]},

    # ——————————————— УРОВЕНЬ 3: МИДЛ ———————————————
    {"level": 3, "text": "Что такое PEP 8?", "answers": ["соглашение", "стиль", "стандарт", "pep8"]},
    {"level": 3, "text": "Как создать виртуальное окружение в Python?", "answers": ["venv", "python -m venv"]},
    {"level": 3, "text": "Что выведет: [1, 2, 3] * 2?", "answers": ["[1, 2, 3, 1, 2, 3]"]},
    {"level": 3, "text": "Как обработать исключение в Python?", "answers": ["try", "except"]},
    {"level": 3, "text": "Что такое list comprehension? Приведи пример.", "answers": ["[", "]"]},

    # ——————————————— УРОВЕНЬ 4: СЕНЬОР ———————————————
    {"level": 4, "text": "Что такое декоратор в Python?", "answers": ["декоратор", "@"]},
    {"level": 4, "text": "Чем отличается 'is' от '=='?", "answers": ["id", "объект", "ссылка", "is сравнивает объекты"]},
    {"level": 4, "text": "Как работает GIL (Global Interpreter Lock)?", "answers": ["gil", "поток", "блокировка", "один поток"]},
    {"level": 4, "text": "Что выведет: a = [1]; b = a; b.append(2); print(a)?", "answers": ["[1, 2]"]},
    {"level": 4, "text": "Как сделать класс итерируемым?", "answers": ["__iter__", "__next__"]},

    # ——————————————— УРОВЕНЬ 5: ЭКСПЕРТ ———————————————
    {"level": 5, "text": "Что такое метакласс в Python?", "answers": ["metaclass", "класс класса"]},
    {"level": 5, "text": "Как работает asyncio и event loop?", "answers": ["асинхрон", "async", "await", "event loop"]},
    {"level": 5, "text": "Чем __new__ отличается от __init__?", "answers": ["__new__", "создание", "инициализация"]},
    {"level": 5, "text": "Как устроена память в Python (например, для малых целых чисел)?", "answers": ["кэш", "-5 до 256", "кэширование"]},
    {"level": 5, "text": "Как реализовать singleton в Python?", "answers": ["singleton", "__new__", "метакласс"]},

    # ——————— ДОПОЛНИТЕЛЬНЫЕ ВОПРОСЫ ———————
    {"level": 2, "text": "Как импортировать модуль json?", "answers": ["import json"]},
    {"level": 3, "text": "Что такое *args и **kwargs?", "answers": ["args", "kwargs", "аргументы"]},
    {"level": 4, "text": "Что такое контекстный менеджер? Как его создать?", "answers": ["with", "__enter__", "__exit__"]},
    {"level": 3, "text": "Как открыть файл для чтения?", "answers": ["open", "r"]},
    {"level": 5, "text": "Что такое descriptor в Python?", "answers": ["descriptor", "__get__", "__set__"]},
    {"level": 4, "text": "Как работает множественное наследование и MRO?", "answers": ["mro", "метод разрешения", "C3"]},
    {"level": 3, "text": "Что выведет: bool([])?", "answers": ["False"]},
]

def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def save_counter(count):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        f.write(str(count))

def is_answer_correct(user_answer, correct_answers):
    """Проверяет, содержится ли хотя бы один правильный ключ в ответе."""
    user = user_answer.strip().lower()
    return any(correct.lower() in user for correct in correct_answers)

def print_certificate(name, level_title, score, max_score, participant_num):
    border = "=" * 60
    percent = (score / max_score) * 100
    print(f"\n{border}")
    print("                🏆 ОФИЦИАЛЬНАЯ ГРАМОТА 🏆")
    print(border)
    print(f"Имя: {name}")
    print(f"Звание: {level_title}")
    print(f"Результат: {score} / {max_score} ({percent:.0f}%)")
    print(f"Ты — {participant_num}-й участник теста!")
    print(border)
    emojis = {
        "Питон-Магистр": "🧙‍♂️ Ты — легенда Python!",
        "Сеньор": "🧠 Ты решаешь задачи, о которых другие мечтают.",
        "Мидл": "🚀 Ты уверенно пишешь код и учишь других.",
        "Джун": "🌱 Ты растёшь как программист — продолжай в том же духе!",
        "Новичок": "🐣 Ты сделал первый шаг в мир Python — это важно!"
    }
    print(emojis.get(level_title, "🐍 Удачи в обучении!"))
    print(border)

def main():
    # Счётчик участников
    total = load_counter() + 1
    save_counter(total)

    print("🐍 ДОБРО ПОЖАЛОВАТЬ В «ОПРЕДЕЛИТЕЛЬ УРОВНЯ PYTHON»! 🐍")
    name = input("Как тебя зовут? > ").strip() or "Анонимный Питонист"
    print(f"\nПривет, {name}! Ты — {total}-й участник этого теста!")
    print("Тебе будет задано 5 случайных вопросов из большой базы знаний.\n")

    # Выбираем 5 случайных вопросов из всей базы
    selected_questions = random.sample(QUESTIONS_DB, k=5)

    score = 0
    for i, q in enumerate(selected_questions, 1):
        print(f"\nВопрос {i}/5 (уровень {q['level']}):")
        print(q["text"])
        user_ans = input("> ")
        if is_answer_correct(user_ans, q["answers"]):
            print("✅ Верно!")
            score += 1
        else:
            print("❌ Неверно. Но это опыт!")

    # Определяем звание по количеству правильных ответов
    if score == 5:
        title = "🧙‍♂️ Питон-Магистр"
    elif score == 4:
        title = "🧠 Сеньор"
    elif score == 3:
        title = "🚀 Мидл"
    elif score == 2:
        title = "🌱 Джун"
    else:
        title = "🐣 Новичок"

    # Анимация
    print("\nОбработка результатов", end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    time.sleep(0.3)

    # Грамота
    print_certificate(name, title, score, 5, total)

if __name__ == "__main__":
    main()