import sys
import argparse
from datetime import datetime
import os

# ЛОГИРОВАНИЕ
# функция create_log создает пустой текстовый файл. Режимы:
# w - открыть на запись (сотрет все, что было),
# a - открыть на дозапись (пишет в конец существующего файла)
# r - открыть на чтение. Если не указать флаг, откроет именно в этом режиме: with open(log_filename) as f:
# encoding='utf-8' означает, что файл создается в кодировке UTF-8
def create_log(log_filename):
    with open(log_filename, 'w', encoding='utf-8') as f:
        pass

# функция write_log записывает в файл строку текстовое сообщение.
# Параметры: text - текстовое сообщение, log_filename - имя файла лога (с полным путем)
def write_log(text, log_filename):
    if text is not None:
        with open(log_filename, 'a', encoding='utf-8') as f:
            f.write("{} {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text))
            f.write("\n")

# матчасть по тому, как работать с датой и временем в python: https://python-scripts.com/datetime-time-python
# все ключи форматирования (Y, m, d и т.д.) в таблице по ссылке: https://pythonworld.ru/moduli/modul-time.html

# ВЫЗОВ СКРИПТА ИЗ КОМАНДНОЙ СТРОКИ С ПАРАМЕТРАМИ
# 1) Матчасть по параметрам командной строки
# 1.1) Запуск скрипта
# Первым пишем название программы, которую мы запускаем. У нас это будет python.exe или просто python. Это еще не параметр
# Скрипт лучше запускать из той директории, в которой он находится.
# Если python.exe определен в системных переменных, можно писать просто python.
# Если нет, придется писать полный путь, например: c:\PythonVenv\vePython36\Scripts\python.exe
# 1.2) Задание параметров
# Первый параметр - имя самого скрипта: *.py. Далее идут все остальные параметры: ключи и их значения, т.е. "настройки" нашего скрипта
# Параметры оформляются следующим образом:
# а) сокращенное название ключа вызываем с одним тире: -d (также бывает /d);
# б) полное название ключа вызываем с двумя тире: --digits, но может встречаться и -digits
# в) после названия ключа идет его значение (если оно есть) через пробел: --digits 4, --logfile d:\tracelog.log
# либо может быть сложнее, например, когда присваивается определенное значение (==)
# примеры из реальной жизни:
# python -m pip install –upgrade pip
# python -m pip install pip==18.1

# 2) Функция main
# Для того, чтобы запущенный из командной строки скрипт работал, в нем должна быть функция main (аналогично С++ и другим языкам)
# Реализация в python:
# 2.1) написать в коде:
'''
if __name__ == "__main__":
  main()
'''
# 2.2) определить функцию main:
'''
def main():
  тело функции
'''
# передача параметров в функцию не требуется, т.к. они уже хранятся в глобальной переменной sys.argv

# 3) Реализация параметров командной строки для скриптов python:
# 3.1) Через простой список параметров sys.argv. Тип: list. Разбор: полностью вручную.
# это аналог передачи списка неименованных параметров неизвестной длины: *args
# Примерная стратегия: находим элемент списка с известным нам названием и берем следующий за ним элемент-значение
'''
args = sys.argv[1:]
if "--digits" in args:
    position = args.index("--digits") + 1
    arg = args[position]
'''

# 3.2) Через модуль argparse, который сделает все это за нас.
# это аналог передачи списка именованных параметров неизвестной длины: **kwargs
#  справка по argparse: https://docs.python.org/2/library/argparse.html
#  как превратить список именованных параметров в словарь: http://qaru.site/questions/53327/what-is-the-right-way-to-treat-python-argparsenamespace-as-a-dictionary vars(args)
'''
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(имя_параметра, тип_параметра, значение_по_умолчанию, описание_параметра)
    return parser
    
def main():
    parser = createParser()
    args = parser.parse_args(sys.argv[1:])
    args.digits - значение параметра "--digits"
    vars(args) - получить все пары "параметр-значение" в виде словаря. точно так же, как для **kwargs
'''
# Важно! В любом из вариантов необходимо исключить первый по счету параметр (имя скрипта): sys.argv[1:]

# создаем парсер, заводим все нужные нам параметры
# плюсы: ключ -h,--help заводить не нужно, он заведется по умолчанию и при неправильном вводе пользователя будет работать самостоятельно, как при запуске любой утилиты Windows или Linux
def createParser():
    parser = argparse.ArgumentParser(description="mai_commandline.py [--digits] [--fullsign] [--partialsign] [--logfile]")
    parser.add_argument("--digits", type=int, default=4,
        help = u"Количество цифр в загаданном числе. Пример: --digits 5. По умолчанию 4 цифры")
    parser.add_argument("--fullsign", default="B", type=str,
        help = u"Каким символом помечать совпадение по значению и месту. Пример: --fullsign F. По умолчанию B")
    parser.add_argument("--partialsign", default="K", type=str,
        help = u"Каким символом помечать совпадение по месту. Пример: --partialsign P. По умолчанию K")
    parser.add_argument("--logfile", default="", help = u"Записывать историю ходов в файл (имя файла). Пример: --logfile c:\guessthenumber.log")
    return parser

# переменная, в которую сохраним имя файла лога
logfile_name = ""

def main():
    # создаем объект парсера командной строки
    parser = createParser()
    # получаем список уже разобранных аргументов (за исключением имени скрипта)
    args = parser.parse_args(sys.argv[1:])
    print(type(args))
    # получаем значение ключа "--digits" - из скольких цифр генерить число в игре. остальные параметры обработаете сами
    if args.digits is not None:
        print(f"Количество цифр, заданное пользователем: {args.digits}")
        digits = args.digits
    # создаем файл лога
    if os.path.exists(args.logfile):
        logfile_name = args.logfile
        create_log(logfile_name)

    # как превратить сисок аргументов в словарь:
    args_dict = vars(args)
    print(f"Аргументы: {args_dict}, тип аргументов: {type(args_dict)}")


if __name__ == "__main__":
    # вот так можно посмотреть аргументы командной строки:
    print(f"Системные аргументы: {sys.argv}, тип: {type(sys.argv)}")

    main()

