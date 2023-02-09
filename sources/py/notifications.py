import time

from datetime import datetime as datef

import asyncio

from main import bot

import groups

import chats

from config import *

import schedule_func

#from telethon.sync import TelegramClient, events

async def check(sleep):
    while True:
        await asyncio.sleep(sleep)

        #async with TelegramClient('name', api_id, api_hash) as client:
        #    print('check!')
        #    user = await client.get_entity('vladyslavbezruk')
        #    print(user.status)

        if datef.today().strftime("%A") not in ['Wednesday', 'Friday', 'Saturday', 'Sunday']:

            date = schedule_func.get_current_date()
            time = schedule_func.get_current_time()

            for code in schedule_func.schedules.keys():
                schedule = schedule_func.get_subj_list(code)
                name = groups.getName(code)

                max = 0

                for subject in schedule:
                    if subject['date'] == date and schedule_func.get_int_time(subject['time_begin']) - time == time_before:
                        answer = f"⁉Заняття для групи {name} відбудеться через {time_before} хв:\n📢{subject['name']}\n🗓{subject['date']}\n👤{subject['teacher']}\n🕐{subject['time_begin']}-{subject['time_end']}\n⏩{subject['url']}"
                        for chat_id in chats.chats.keys():
                            if name in chats.chats[chat_id]:
                                await bot.send_message(chat_id=chat_id, text=answer)

                    if subject['date'] == date and schedule_func.get_int_time(subject['time_end']) > max:
                        max = schedule_func.get_int_time(subject['time_end'])

                if max == time and max > 0:
                    for chat_id in chats.chats.keys():
                        if name in chats.chats[chat_id]:
                            await bot.send_message(chat_id=chat_id, text=f"⁉Заняття для групи {name} закінчились!")
                elif max == time and max == 0:
                    for chat_id in chats.chats.keys():
                        if name in chats.chats[chat_id]:
                            await bot.send_message(chat_id=chat_id, text=f"⁉Сьогодні немає занять для групи {name}!")
