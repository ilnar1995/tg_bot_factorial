import os

from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = os.environ.get("token")
results = [1] * 2
cache = {}


def factorial(begin, n, thread, results):
    if n == begin:
        if thread == 'thread1':
            results[0] = begin
        if thread == 'thread2':
            results[1] = begin
        return begin
    else:
        result = n * factorial(begin, n - 1, thread, results)

    if thread == 'thread1':
        results[0] = result
    if thread == 'thread2':
        results[1] = result

    return result


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Введите число, чтобы посчитать факториал.")


def factorial_command(update, context):
    try:
        number = int(update.message.text)
    except (ValueError, IndexError):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка ввода! Введите целое число.")
    else:

        if number < 1 or number > 40:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Число должно быть положительным и меньше 41")
        else:
            mid = number // 2
            # проверяем кэш
            if number in cache:
                _factorial = cache[number]
            else:
                if number == 1:
                    results[0], results[1] = 1, 1
                else:
                    thread1 = Thread(target=factorial, args=(1, mid, 'thread1', results))
                    thread2 = Thread(target=factorial, args=(mid + 1, number, 'thread2', results))

                    # Запускаем потоки
                    thread1.start()
                    thread2.start()

                    # Ожидаем завершения потоков
                    thread1.join()
                    thread2.join()
                _factorial = results[0] * results[1]
                # добавляем в кэш
                cache[number] = _factorial

            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Факториал равен: {_factorial}")


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
factorial_handler = MessageHandler(Filters.text & ~Filters.command, factorial_command)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(factorial_handler)

updater.start_polling()
updater.idle()

