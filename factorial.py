from threading import Thread

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



from telegram.ext import Updater, CommandHandler

token = '6400511901:AAFcZLKloLe60r1L2IeKw1Gb4ALisyQRc4E'
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Введите число, чтобы посчитать факториал.")

def factorial_command(update, context):
    try:
        number = int(context.args[0])

        mid = number//2

        if number in cache:
            _factorial = cache[n]
        else:
            if number == 1:
                results[0], results[1] = 1, 1
            else:
                thread1 = Thread(target=factorial, args=(1, mid, 'thread1', results))
                thread2 = Thread(target=factorial, args=(mid+1, number, 'thread2', results))

                # Запускаем потоки
                thread1.start()
                thread2.start()

                # Ожидаем завершения потоков
                thread1.join()
                thread2.join()
            _factorial = results[0] * results[1]
            cache[number] = _factorial

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Факториал равен: {_factorial}")

    except (ValueError, IndexError):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка ввода! Введите целое число.")

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
factorial_handler = CommandHandler('factorial', factorial_command)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(factorial_handler)

updater.start_polling()