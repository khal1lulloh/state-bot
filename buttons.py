from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
from cldb import Sql
db = Sql()
start_bosilgandagi= InlineKeyboardMarkup(
	inline_keyboard=[

		[
			InlineKeyboardButton(text="📝 Kursga yozilish", callback_data="kursga_yozilish"),	
		],
	],
) 
canal = InlineKeyboardMarkup(
	inline_keyboard=[
	[
		InlineKeyboardButton(text="📣 Habel education", url="https://t.me/+bVty8FbyMBUyNDJh")
	],
	[
		InlineKeyboardButton(text="✔️ Obuna bo'ldim",callback_data="check")
	],
	],
)



contact = ReplyKeyboardMarkup(
	keyboard = [
		[
			KeyboardButton(text='Raqamini yuborish',request_contact=True),  #request_contact=True
		],
	],
	resize_keyboard=True, one_time_keyboard=True
)

tasdiqlash= InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="✅ Xa", callback_data="xa"),
			InlineKeyboardButton(text="❌ Yuq", callback_data="yuq")
		],
	],
) 


reklamatasdiqlash= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Xa", callback_data="reklamaruxsat"),
            InlineKeyboardButton(text="❌ Yuq", callback_data="reklamaruxsatyuq")
        ],
    ],
) 


menu = InlineKeyboardMarkup(
  inline_keyboard = [
  [
  	InlineKeyboardButton(text="Dispatch",callback_data="disp"),
    InlineKeyboardButton(text="Statistics",callback_data="stats"),
    InlineKeyboardButton(text="Courses",callback_data="course")
  ],
  ]
)


menu1 = InlineKeyboardMarkup(
  inline_keyboard = [
  [
  	InlineKeyboardButton(text="New",callback_data="add"),
    InlineKeyboardButton(text="Edit",callback_data="edit"),
    InlineKeyboardButton(text="Delete",callback_data="del")
  ],
  [
  InlineKeyboardButton(text="🔙 Ortga",callback_data="orqa2")
  ],

  ]
)

menu2 = InlineKeyboardMarkup(
  inline_keyboard = [
  [
  	InlineKeyboardButton(text="start",callback_data="start"),
    InlineKeyboardButton(text="phone",callback_data="phone"),
    # InlineKeyboardButton(text="course",callback_data="courses")
  ],
  [
  InlineKeyboardButton(text="🔙 Ortga",callback_data="orqa")
  ],
  ]
)

menu3 = InlineKeyboardMarkup(
  inline_keyboard = [
  [
  	InlineKeyboardButton(text="start",callback_data="starts"),
    InlineKeyboardButton(text="phone",callback_data="phones"),
    # InlineKeyboardButton(text="course",callback_data="courses")
  ],
  [
  InlineKeyboardButton(text="🔙 Ortga",callback_data="orqa")
  ],
  ]
)



tasdiqlash1= InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="✅ Xa", callback_data="xa1"),
			InlineKeyboardButton(text="❌ Yoq", callback_data="yuq1")
		],
	],
) 

tasdiqlash2= InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="✅ Xa", callback_data="addd"),
			InlineKeyboardButton(text="❌ Yuq", callback_data="nooo")
		],
	],
) 
async def for_keyboard():
	markup = InlineKeyboardMarkup(row_width=3)
	x = db.select_all()
	for i in x:
		button_text = i[0]
		callback_data = i[0]
		markup.insert(
   		InlineKeyboardButton(text=button_text, callback_data=callback_data)
   		)
	# markup.add(
	# 	InlineKeyboardButton(text='🔙 Ortga', callback_data="orqa1")
	# )

	return markup

async def for_keyboard_ochirish():
	mark = InlineKeyboardMarkup(row_width=3)
	x = db.select_all()
	for i in x:
		button_text = i[0]
		callback_data = i[0]
		mark.insert(
   		InlineKeyboardButton(text=button_text, callback_data=f"del{callback_data}")
   		)
	# mark.add(
	# 	InlineKeyboardButton(text='🔙 Ortga', callback_data="orqa1")
	# )
	return mark

async def for_keyboard_malumot():
	marsh = InlineKeyboardMarkup(row_width=3)
	x = db.select_all()
	for i in x:
		button_text = i[0]
		callback_data = i[0]
		marsh.insert(
   		InlineKeyboardButton(text=button_text, callback_data=f"mal{callback_data}")
   		)
	return marsh