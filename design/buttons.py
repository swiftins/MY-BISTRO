from math import ceil
import telebot
from telebot import types



def create_tile_kbd(keyboard,
                    row_width=1,
                    nums=1,
                    msg=["", "",],
                    splitter="",
                    values=None,
                    back ="❌",
                    keys = []):

    """
    Универсальная функция для создания плиточной клавиатуры.
    Работает с ReplyKeyboardMarkup и InlineKeyboardMarkup.

    Параметры:
    - keyboard: Экземпляр клавиатуры (ReplyKeyboardMarkup или InlineKeyboardMarkup).
    - row_width: Количество кнопок в строке (по умолчанию 1).
    - nums: Количество кнопок для создания (по умолчанию 1).
    - msg: Список из двух строк, которые будут добавлены к тексту кнопки (по умолчанию ["", ""]).
    - splitter: Разделитель между частями текста кнопки (по умолчанию "").
    - values: Список значений для текста кнопок или одиночное значение (по умолчанию None).
    - back: Если не None, то 0-ое значение заменяется на значение back
    - keys: Значения callback для Inline кнопок, присваиваются, если не None

    Возвращает:
    - Клавиатуру с добавленными кнопками.
    """
    if isinstance(keyboard, types.ReplyKeyboardMarkup):
        # Для обычных кнопок по умолчанию используем KeyboardButton
        btntype = types.KeyboardButton
    elif isinstance(keyboard, types.InlineKeyboardMarkup):
        # Для инлайн-кнопок используем InlineKeyboardButton
        btntype = types.InlineKeyboardButton
    else:
        raise TypeError("keyboard должен быть либо ReplyKeyboardMarkup, либо InlineKeyboardMarkup")

    # Создаем кнопки в виде плитки
    if values:
        if type(values) == list:
            if back:
                values = [back,] + values
        else:
            if back:
                values = [back, values]
            else:
                values = [values]
        nums = len(values)
    rows = ceil(nums / row_width)

    for i in range(rows):
        btns = []
        if (nums - (i + 1) * row_width) >= 0:
            columns = row_width
        else:
            columns = nums % row_width

        for j in range(columns):
            val = (i) * row_width + j
            if back and val == 0:
                text = back
            elif type(values) == list:
                text = values[val]
            else:
                text = f"{msg[0]}{splitter}{val}{splitter}{msg[1]}"

            # Если это Inline кнопка, добавляем callback_data
            if btntype == types.InlineKeyboardButton:
                if val <= len(keys) -1:
                    val = keys[val]
                btns.append(btntype(text, callback_data=f"{val}"))
            else:
                btns.append(btntype(text))

        keyboard.row(*btns)

    return keyboard

def create_reply_kbd(row_width=2, values=[], back ="X", keys = []):
    """
    Создает Reply клавиатуру с плиточными кнопками.

    Параметры:
    - row_width: Количество кнопок в строке (по умолчанию 2).
    - values: Список значений для текста кнопок (по умолчанию []).

    Возвращает:
    - Reply клавиатуру с добавленными кнопками.
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    create_tile_kbd(keyboard, row_width=row_width, msg=["Категория ", ""], values=values, back=back, keys = keys)
    return keyboard

def create_inline_kbd(row_width=3, nums=3, values=None,msg=["",""], keys=[]):
    """
    Создает Inline клавиатуру с плиточными кнопками.

    Параметры:
    - row_width: Количество кнопок в строке (по умолчанию 3).
    - nums: Количество кнопок для создания (по умолчанию 3).
    - values: Список значений для текста кнопок или одиночное значение (по умолчанию None).

    Возвращает:
    - Inline клавиатуру с добавленными кнопками.
    """
    keyboard = types.InlineKeyboardMarkup( row_width=row_width)
    create_tile_kbd(keyboard, row_width=row_width, nums=nums, msg=msg, values=values, keys = keys)
    return keyboard

# формируем клавиатуру с кнопками из массива строк
def create_keyboard_variable_rows(data):
    keyboard = types.InlineKeyboardMarkup(row_width=len(data[0])+1)
    for index, row in enumerate(data):
        row_showing = [row[1],f"{row[2]} руб.*{row[3]}"]
        buttons = [types.InlineKeyboardButton(text=col, callback_data="noop") for col in row_showing]
        buttons.append(types.InlineKeyboardButton(text="❌", callback_data=f"delete_{row[0]}"))
        keyboard.add(*buttons)
    buttons = [types.InlineKeyboardButton(text=col, callback_data=col) for col in ["Оплатить","Назад"]]
    keyboard.add(*buttons)
    return keyboard
