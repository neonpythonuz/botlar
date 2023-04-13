from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from states.holatlar import Tanlov, Korzinka
from keyboards.default.menu_uchun import menu_buttons, tasdiqlash_buttons
from loader import dp, base, bot



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)

menular = base.select_all_menu()
print(menular)
@dp.message_handler(text = [menu[1] for menu in menular])
async def bot_start(message: types.Message):
    menu_nomi = message.text
    tanlangan_menu = base.select_mahsulot(tur=menu_nomi)
    index = 0
    keys = []
    j = 0
    print(tanlangan_menu)
    for menu in tanlangan_menu:
        print(menu)
        if j % 2 == 0 and j != 0:
            index += 1
        if j % 2 == 0:
            keys.append([KeyboardButton(text=f"{menu[0]}", )])
        else:
            keys[index].append(KeyboardButton(text=f"{menu[0]}", ))
        j += 1
    keys.append([KeyboardButton(text='Ortga')])
    menu_buttons = ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True)
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)
    await Tanlov.mahsulot_tanlash_holati.set()

@dp.message_handler(text= 'Ortga',state=Tanlov.mahsulot_tanlash_holati)
async def bot_start(message: types.Message,state:FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)
    await state.finish()

@dp.message_handler(commands='start',state=Tanlov.mahsulot_tanlash_holati)
async def bot_start(message: types.Message,state:FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)
    await state.finish()

mahsulotlar = base.select_all_mahsulotlar()
@dp.message_handler(text=[mahsulot[0] for mahsulot in mahsulotlar] ,state=Tanlov.mahsulot_tanlash_holati)
async def bot_start(message: types.Message):
    mahsulot_nomi = message.text
    mahsulot = base.select_mahsulot_only(nomi=mahsulot_nomi)
    mahsulot_id = mahsulot[0]
    nomi = mahsulot[1]
    narxi = mahsulot[2]
    rasm_link = mahsulot[3]
    kg = mahsulot[6]
    s = f"Kg : {kg}"
    if not kg:
        kg = mahsulot[7]
        s = f"Litr : {kg}"

        user_id = message.from_user.id

        await bot.send_photo(chat_id=user_id, photo=rasm_link, caption=f"Nomi : {nomi}\n"
                                                                       f"Narxi : {narxi}\n"
                                                                    f"{s}",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=
                                                           [[InlineKeyboardButton(text="Sotib olish", callback_data=f'{mahsulot_id}')]]))
    else:

        user_id = message.from_user.id

        await bot.send_photo(chat_id=user_id, photo=rasm_link, caption=f"Nomi : {nomi}\n"
                                                                       f"Narxi : {narxi}\n"
                                                                       f"{s}",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=
                                                               [[InlineKeyboardButton(text="Sotib olish",
                                                                                      callback_data=f'{mahsulot_id}')]]))
    await Tanlov.sotib_olish_holati.set()


@dp.callback_query_handler(state=Tanlov.sotib_olish_holati)
async def bot_start(xabar: CallbackQuery, state:FSMContext):
    mahsulot_id = xabar.data
    user_id = xabar.from_user.id
    """
    (2, 'Lagmon', 24000, 'https://t.me/textdoofine/315', 'Taomlar', None, 1, None)
    
    """
    mahsulot = base.select_mahsulot_only(id = mahsulot_id)
    mahsulot_nomi = mahsulot[1]
    mahsulot_narxi = mahsulot[2]
    tekshirish = base.count_mahsulot(nomi=mahsulot_nomi,tg_id=user_id)
    print("nnnnnnnnn")
    print((tekshirish ))
    print("nnnnnnnnn")

    if not tekshirish:
        mahsulot_narxi = mahsulot[2]
        mahsulot_rasmi = mahsulot[3]
        mahsulot_soni = 1
        user_id = xabar.from_user.id
        ism = xabar.from_user.first_name
        base.add_mahsulot_to_korzinka(nomi=mahsulot_nomi, narxi=mahsulot_narxi, soni=mahsulot_soni, rasm=mahsulot_rasmi, tg_id=user_id, ism=ism)
        await xabar.message.answer(text=f"mahsult xarid qilindi yana mahsulot tanlang ..{1}.")
    else:
        new_soni = tekshirish[0] +1
        base.update_user_korzinka(soni=new_soni, tg_id=user_id, nomi=mahsulot_nomi)
        await xabar.message.answer(text=f"mahsult xarid qilindi yana mahsulot tanlang ..{new_soni}.")
    await Tanlov.mahsulot_tanlash_holati.set()


@dp.message_handler(text="Korzinka")
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    products = base.select_mahsulotlar_from_korzinka(tg_id = user_id)
    print(products)
    for mahsulot in products:
        """
        (6, 'Bishteks', 15000, 'https://t.me/textdoofine/315', 2, 789362160, '💢')
        """
        mahsulot_id = mahsulot[0]
        nomi = mahsulot[1]
        narxi = mahsulot[2]
        rasm_link = mahsulot[3]
        soni = mahsulot[4]
        user_id = message.from_user.id

        await bot.send_photo(chat_id=user_id, photo=rasm_link, caption=f"Nomi : {nomi}\n"
                                                                       f"Narxi : {narxi}\n"
                                                                       f"Soni : {soni}",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                     InlineKeyboardButton(text='+', callback_data=f'add{mahsulot_id}'),
                                     InlineKeyboardButton(text='-', callback_data=f'sub{mahsulot_id}')
                                 ],
                                 [
                                     InlineKeyboardButton(text="O'chirish", callback_data=f'del{mahsulot_id}')
                                 ]
                             ]))
    await bot.send_message(chat_id=user_id,text="Sotib olish uchun tasdiqlash tugmasini tanlang",reply_markup=tasdiqlash_buttons)
    await Korzinka.update_holati.set()


@dp.message_handler(text="Bekor qilish", state=Korzinka.update_holati)
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id,text="Bekor qilindi",reply_markup=menu_buttons)
    base.delet_mahsulot_from_korzinka(tg_id=user_id)
    await state.finish()


@dp.message_handler(text="Tasdiqlash", state=Korzinka.update_holati)
async def bot_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    products = base.select_mahsulotlar_from_korzinka(tg_id = user_id)
    matn = ''
    yigindi = 0
    for mahsulot in products:
        """
        (6, 'Bishteks', 15000, 'https://t.me/textdoofine/315', 2, 789362160, '💢')
        """
        mahsulot_id = mahsulot[0]
        nomi = mahsulot[1]
        narxi = mahsulot[2]
        rasm_link = mahsulot[3]
        soni = mahsulot[4]
        user_id = message.from_user.id
        matn += f"Nomi : {nomi}     Narxi : {narxi}      Soni : {soni}    Umumiy narxi : {narxi*soni} so'm \n"
        yigindi += narxi*soni
    matn += f"Umumiy summa : {yigindi} \n"
    await bot.send_message(chat_id=user_id,text=matn, reply_markup=menu_buttons)
    matn += f"Ismi : {message.from_user.first_name}     Username : @{message.from_user.username}"
    await bot.send_message(chat_id='789362160', text=matn)
    base.delet_mahsulot_from_korzinka(tg_id=user_id)
    await state.finish()

@dp.callback_query_handler(state=Korzinka.update_holati)
async def bot_start(xabar: CallbackQuery,state:FSMContext):
    malumot = str(xabar.data)[:3]
    print(malumot)
    mahsulot_id = str(xabar.data)[3:]
    user_id = xabar.from_user.id
    mahsulot = base.select_mahsulot_from_korzinka_only(id=mahsulot_id)
    mahsulot_nomi = mahsulot[1]
    tekshirish = base.count_mahsulot(tg_id=user_id, nomi=mahsulot_nomi)
    print('tekshirish')

    print(tekshirish)
    if malumot == 'add':
        new_soni = tekshirish[0] + 1
        base.update_user_korzinka(soni=new_soni, tg_id=user_id, nomi=mahsulot_nomi)
    elif malumot == 'sub':
        new_soni = tekshirish[0] - 1
        base.update_user_korzinka(soni=new_soni, tg_id=user_id, nomi=mahsulot_nomi)
    elif malumot == 'del':
        base.delet_mahsulot_from_korzinka(tg_id=user_id, nomi=mahsulot_nomi)
    await xabar.message.answer(text=f'{malumot}')
    await Korzinka.update_holati.set()


@dp.message_handler(text= 'Ortga',state=Korzinka.update_holati)
async def bot_start(message: types.Message,state:FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)
    await state.finish()

@dp.message_handler(commands='start',state=Korzinka.update_holati)
async def bot_start(message: types.Message,state:FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)
    await state.finish()

@dp.message_handler(text= 'Korzinka',state=Korzinka.update_holati)
async def bot_start(message: types.Message,state:FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu_buttons)
    await state.finish()
