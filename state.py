from aiogram.dispatcher.filters.state import StatesGroup, State

class KursData(StatesGroup):
	ism = State()
	telefon = State()

class AddKurs(StatesGroup):
	nomi = State()
	izoh = State()
	narxi = State()

class EditKurs(StatesGroup):
	izoh = State()
	narxi = State()

class Dispatch(StatesGroup):
	xabar = State()