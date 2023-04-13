from aiogram.dispatcher.filters.state import State, StatesGroup

class Tanlov(StatesGroup):
    mahsulot_tanlash_holati = State()
    sotib_olish_holati = State()

class Korzinka(StatesGroup):
    update_holati = State()
