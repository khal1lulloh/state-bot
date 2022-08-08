import logging
from config import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

from aiogram.dispatcher import FSMContext
from state import KursData, AddKurs, EditKurs, Dispatch
from buttons import *
from aiogram.types import Message, CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cldb import Sql
from typing import Union
storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=Token)
dp = Dispatcher(bot,storage=storage)
db = Sql()
admin = 692799479

def checking(chat_member):
   if chat_member['status'] != 'left':
      return True
   else:
      return False

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   db.add_kurs()
   db.tablitsa_yaratish()
   global marsh, idi
   user = message.from_user.username
   marsh = await for_keyboard_malumot()
   idi = message.from_user.id
   await message.reply(f"Assalomu aleykum, {message.from_user.first_name}!\n\nBu bot orqali bizning o'quv markazimizdagi kurslar xaqida ma'lumot olishingiz va kurslarga yozilishingiz mumkin!",parse_mode='HTML')
   if checking(await bot.get_chat_member(chat_id="@avlod22",user_id = idi)):
      global data1
      data1 = db.id_user(idi)
      if data1 is None:
         db.tablitsa_qushish(idi,user)
         await message.answer("😊 Marhamat, kurslarimiz xaqida ma'lumotlarni olishingiz mumkin:",reply_markup=marsh)
      else:
         await message.answer("😊 Marhamat, kurslarimiz xaqida ma'lumotlarni ko'rishingiz mumkin:",reply_markup=marsh)
   else:
      await message.answer("<b>Botdan to'liq foydalanish uchun quyidagi kanalga obuna bo'ling</b>",parse_mode='HTML',reply_markup=canal)

#checking
@dp.callback_query_handler(text="check")
async def check(call: CallbackQuery):
   if checking(await bot.get_chat_member(chat_id="@avlod22",user_id=idi)):
      global data1
      data1 = db.id_user(idi)
      if data1 is None:
         db.tablitsa_qushish(idi,user)
         await call.message.answer("😊 Marhamat, kurslarimiz xaqida ma'lumotlarni olishingiz mumkin:",reply_markup=marsh)
      else:
         await call.message.answer("😊 Marhamat, kurslarimiz xaqida ma'lumotlarni ko'rishingiz mumkin:",reply_markup=marsh)
   else:
      await call.answer("Avval kanalga obuna bo'ling", show_alert=True)
  
# state
@dp.callback_query_handler(text="kursga_yozilish",states=None)
async def uquv_markazlar_func(call: CallbackQuery):
   await call.message.answer("<b>✍️ To'liq ismingizni kiriting</b>",parse_mode='HTML')
   await KursData.ism.set()

# ism
@dp.message_handler(state=KursData.ism)
async def answer_fullname(message: types.Message, state: FSMContext):
   ism = message.text.title()
   await state.update_data(
      {"ismfam": ism}
   ) 
   await message.answer("<b>📞 Telefon raqamingizni yuboring</b>",parse_mode='HTML', reply_markup=contact)
   await KursData.next()

# contact
@dp.message_handler(content_types='contact',state=KursData.telefon)
async def get_contact(message: Message, state: FSMContext):
   telefon = message.contact.phone_number
   await state.update_data(
      {"telefon_raqam": telefon}
   )
   data = await state.get_data()
   global name,raqam
   name = data.get("ismfam")
   raqam = data.get("telefon_raqam")
   p = "<b>Ma'lumotlaringiz to'g'rimi?</b>\n\n"
   p += f"<b>F.I.O:</b> {name}\n<b>TEL:</b> {raqam}"

   await message.answer(p,parse_mode='HTML',reply_markup=tasdiqlash)
   await state.finish()
   await state.reset_state()


@dp.callback_query_handler(text="xa")
async def uquv_markazlar_func(call: CallbackQuery):
   db.tablitsa_uz(idi,name,raqam)
   await call.message.answer("<b>✅ Ma'lumotlaringiz qabul qilindi </b>",parse_mode="HTML")
   await call.message.delete()

@dp.callback_query_handler(text="yuq")
async def uquv_markazlar_func(call: CallbackQuery):
   await call.message.answer("<b> Ma'lumotlaringiz o'chirildi 🔥 </b>",reply_markup=start_bosilgandagi,parse_mode="HTML")
   await call.message.delete()


@dp.message_handler(text="/admin", user_id=admin)
async def send_welcome(message: types.Message):
   await message.answer("<b>Admin, xush kelibsiz!</b>",reply_markup=menu,parse_mode='HTML')



# dispatch
@dp.callback_query_handler(text="disp")
async def uquv_markazlar_func19(call: CallbackQuery):
   await call.message.answer("Kimga dispatch qilamiz?:",reply_markup=menu3)
   await call.message.delete()

@dp.callback_query_handler(text="starts",states=None)
async def uquv_markazlar_func19(call: CallbackQuery):
   await call.message.answer("Xabarni kiriting:")
   await Dispatch.xabar.set()

@dp.message_handler(state=Dispatch.xabar)
async def answer(message: types.Message, state: FSMContext):
   xab = message.text
   await state.update_data(
      {"xabar": xab}
   ) 
   date = await state.get_data()
   global habar
   habar = date.get("xabar")
   p = "Xabar tog'ri kiritilganmi?\n\n"
   p += f"<b>Xabar</b>: {habar}"

   await message.answer(p,parse_mode='HTML',reply_markup=reklamatasdiqlash)
   await state.finish()
   await state.reset_state()

@dp.callback_query_handler(text="reklamaruxsat")
async def uquv_markazlar(call: CallbackQuery):
   t = db.rec()
   for i in t:
      date2 = i[0]
   await bot.send_message(chat_id=date2,text=habar)
   await call.message.answer("<b>✅ Xabar yuborildi </b>",parse_mode="HTML",reply_markup=menu3)
   await call.message.delete()


@dp.callback_query_handler(text="reklamaruxsatyuq")
async def uquv_markazlar_func(call: CallbackQuery):
   await call.message.answer("<b> Xabar o'chirildi 🔥 </b>",parse_mode="HTML",reply_markup=menu3)
   await call.message.delete()


# @dp.message_handler(commands=['ads'],user_id=692799479)
# async def send_welcome(message: types.Message):
#     q = w.rec()
#     e = message.text[5::]
#     for k in q:
#         data2 = k[0]
#         await bot.send_message(chat_id=data2,text=e)


# statistics
@dp.callback_query_handler(text="stats")
async def uquv_markazlar_func19(call: CallbackQuery):
   await call.message.answer("Foydalanuvchilar sonini qaysi bosqichda bilvoqchisiz?:",reply_markup=menu2)
   await call.message.delete()

@dp.callback_query_handler(text="start")
async def user(call: CallbackQuery):
   d = db.userlar()
   await call.message.answer(f"Foydalanuvchilar: {d} ta")
   await call.message.delete()

@dp.callback_query_handler(text="phone")
async def user2(call: CallbackQuery):
   d = db.telefonlar()
   await call.message.answer(f"Nomer qoldirganlar: {d} ta")
   await call.message.delete()

@dp.callback_query_handler(text="orqa")
async def user3(call: CallbackQuery):
   await call.message.answer("Qaysi vazifani bajaramiz?",reply_markup=menu)

# course
@dp.callback_query_handler(text="course")
async def uquv_markazlar_func(call: CallbackQuery):
   await call.message.answer("Tanlang",reply_markup=menu1)
   await call.message.delete()

@dp.callback_query_handler(text="orqa2")
async def user3(call: CallbackQuery):
   await call.message.answer("Qaysi vazifani bajaramiz?",reply_markup=menu)

# addcourse
@dp.callback_query_handler(text="add",states=None)
async def uquv_markazlar_func(call: CallbackQuery):
   await call.message.answer("<b>Kurs nomini kiriting:</b>",parse_mode='HTML')
   await AddKurs.nomi.set()

# ism
@dp.message_handler(state=AddKurs.nomi)
async def answer_fullname(message: types.Message, state: FSMContext):
   nomi = message.text
   await state.update_data(
      {"kursnomi": nomi}
   ) 
   await message.answer("<b>Izohini kiriting:</b>",parse_mode='HTML')
   await AddKurs.next()


@dp.message_handler(state=AddKurs.izoh)
async def get_contact(message: Message, state: FSMContext):
   izoh = message.text
   await state.update_data(
      {"kursizoh": izoh}
   )
   await message.answer("<b>Narxini kiriting:</b>",parse_mode='HTML')
   await AddKurs.next()

@dp.message_handler(state=AddKurs.narxi)
async def get_contact(message: Message, state: FSMContext):
   narxi = message.text
   await state.update_data(
      {"kursnarxi": narxi}
   )

   data = await state.get_data()
   global nom,izoh,narx
   nom = data.get("kursnomi")
   izoh = data.get("kursizoh")
   narx = data.get('kursnarxi')
   p = "Ma'lumotlar to'g'rimi?\n\n"
   p += f"<b>Kurs nomi:</b> {nom}\n<b>Izoh:</b> {izoh}\n<b>Narxi:</b> {narx} so'm"

   await message.answer(p,parse_mode='HTML',reply_markup=tasdiqlash1)
   await state.finish()
   await state.reset_state()

@dp.callback_query_handler(text="xa1")
async def uquv_markazlar_func(call: CallbackQuery):
   db.kurs(nom,izoh,narx)
   await call.message.answer("<b>✅ Kurs qo'shildi </b>",parse_mode="HTML",reply_markup=menu1)
   await call.message.delete()


@dp.callback_query_handler(text="yuq1")
async def uquv_markazlar_func(call: CallbackQuery):
   await call.message.answer("<b> Kurs o'chirildi 🔥 </b>",parse_mode="HTML",reply_markup=menu1)
   await call.message.delete()

# edit
# addcourse


@dp.callback_query_handler(text="edit")
async def uquv_markazlar_func(call: CallbackQuery):
   global markup
   markup = await for_keyboard()
   await call.message.answer("Tanlang: ",reply_markup=markup)
   await call.message.delete()

@dp.callback_query_handler(text="del")
async def uquv_markazlar_func(call: CallbackQuery):
   global mark
   mark = await for_keyboard_ochirish()
   await call.message.answer("Tanlang: ",reply_markup=mark)
   await call.message.delete()

@dp.callback_query_handler()
async def byuing_pear(call: CallbackQuery):
   global v
   v = call.data
   data = db.select_all()
   for i in data:
      n = i[0]
      if v == n:
         await uquv(call,v)
   if v[0:3] == 'del':
      await uquv2(call,v)
   if v[0:3] == 'mal':
      await uquv3(call,v)

#ma'lumot chqarish
async def uquv3(call,v):
   w = v[3:]
   info = db.sel(v[3:])
   info2 = db.sell(v[3:])
   n = ''
   q = info2[0]
   for j in info:
      n = j[0]
   await call.message.answer(f"<b>{w}</b>\n\n{n}\n\nNarxi: {q} so'm",parse_mode='HTML')
         
#delete
async def uquv2(call,v):
   await bot.send_message(admin,db.ochirish(v[3:]))


# edit kurs
async def uquv(call,v,states=None):
   await call.message.answer('<b>Izohini kiriting:</b>',parse_mode='HTML')
   await EditKurs.izoh.set()

@dp.message_handler(state=EditKurs.izoh)
async def get_contact(message: Message, state: FSMContext):
   editizoh = message.text
   await state.update_data(
      {"editizoh": editizoh}
   )
   await message.answer("<b>Narxi</b>",parse_mode='HTML')
   await EditKurs.next()

@dp.message_handler(state=EditKurs.narxi)
async def get_contact(message: Message, state: FSMContext):
   editnarxi = message.text
   await state.update_data(
      {"editnarxi": editnarxi}
   )
   data = await state.get_data()
   global editizoh1, editnarx1
   editizoh1 = data.get("editizoh")
   editnarx1 = data.get('editnarxi')
   p = "Ma'lumotlaringiz to'g'rimi?\n\n"
   p += f"Izoh: {editizoh1}\nNarx: {editnarx1}"
   

   db.edit_kurs(v,editizoh1,editnarx1)
   await message.answer("<b>O'zgartirildi  ✅</b>",parse_mode='HTML')
   await message.answer("Qanday vazifani bajarmoqchisiz?",reply_markup=menu1)
   await state.finish()
   await state.reset_state()

#ortga knopkalari
# @dp.callback_query_handler(text="orqa1")
# async def uquv_markazlar_func15(call: CallbackQuery):
#    await call.message.answer("Qanday vazifani bajarmoqchisiz?",reply_markup=menu1)
#    await call.message.delete()


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)

