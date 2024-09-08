import wifipythonroute
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import logging
import token
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=f"{token.tok}")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! Это бот для управления роутером, вот мои команды")
    await message.answer('/info_device')
    await message.answer('/info_wan')
    await message.answer('/local_users')
    await message.answer('/okr_sreda')
    await message.answer('/parent_ctrl')


# Хэндлер на команду /test1
@dp.message(Command("info_device"))
async def info_dev(message: types.Message):
    inf_list = wifipythonroute.info_device()
    await message.answer('Вот информация об устройстве')
    for i in inf_list:
        await message.answer(i)


@dp.message(Command('info_wan'))
async def info_wn(message: types.Message):
    infwan_list = wifipythonroute.status_wan()
    await message.answer('Вот информация о WAN')
    for i in infwan_list:
        await message.answer(i)


@dp.message(Command('local_users'))
async def locl_usr(message: types.Message):
    list_local = wifipythonroute.list_local_user()
    await message.answer('Вот список подключённых устройств')
    for i in range(len(list_local)):
        await message.answer(f'{i}: {list_local[i]}')


@dp.message(Command('okr_sreda'))
async def ok_sred(message: types.Message):
    g2_4, g_5 = wifipythonroute.okr_sreda()
    await message.answer('2.4G точки вокруг')
    for i in g2_4:
        rout = ''
        for j in i:
            rout = rout + ' ' + j + ';'
        await message.answer(rout)
    await message.answer('5G точки вокруг')
    for i in g_5:
        rout = ''
        for j in i:
            rout = rout + ' ' + j + ';'
        await message.answer(rout)


@dp.message(Command("parent_ctrl"))
async def otv(message: types.Message):
    global idm
    await message.answer('Введите данные жертвы в формате (name(любое) a1:a1:a1:a1:a1:a1(mac адрес) 1(1-включить ''интернет 0-выключить)) пример: alex a1:d5:fc:a3:3e:7a 1')
    idm = str(int(message.message_id) + 2)


@dp.message()
async def mes(message: types.Message):
    global txt
    if str(message.message_id) == idm:
        txt = message.text.split()
        lis, res = wifipythonroute.parent_control(txt[0], txt[1], int(txt[2]))
        await message.answer('Список выключеных устройств')
        for i in lis:
            await message.answer(i)
        await message.answer(f'Результат выполнения: {res}')

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


asyncio.run(main())
