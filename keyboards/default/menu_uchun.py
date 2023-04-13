from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import base
menular = base.select_all_menu()
print(menular)

index = 0
keys = []
j = 0
regions = base.select_all_menu()
for region in regions:
    if j % 2 == 0 and j != 0:
        index += 1
    if j % 2 == 0:
        keys.append([KeyboardButton(text=f"{region[1]}",)])
    else:
        keys[index].append(KeyboardButton(text=f"{region[1]}",))
    j += 1
keys.append([KeyboardButton(text='Ortga')])
keys.append([KeyboardButton(text='Korzinka')])
menu_buttons = ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True)

tasdiqlash_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tasdiqlash"),
            KeyboardButton(text="Bekor qilish")
        ]
    ],
    resize_keyboard=True
)






