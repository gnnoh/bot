import asyncio
import logging
import os

from aiogram import types, executor

from core.bots.aiogram.client import dp
from core.bots.aiogram.message import MessageSession, FetchTarget
from core.bots.aiogram.tasks import MessageTaskManager, FinishedTasks
from core.elements import MsgInfo, Session, Command, Schedule
from core.loader import Modules
from core.parser.message import parser
from core.scheduler import Scheduler
from core.utils import PrivateAssets, init, load_prompt

PrivateAssets.set(os.path.abspath(os.path.dirname(__file__) + '/assets'))
init()


@dp.message_handler()
async def msg_handler(message: types.Message):
    all_tsk = MessageTaskManager.get()
    user_id = message.from_user.id
    if user_id in all_tsk:
        FinishedTasks.add_task(user_id, message)
        all_tsk[user_id].set()
        MessageTaskManager.del_task(user_id)
    msg = MessageSession(MsgInfo(targetId=f'Telegram|{message.chat.type}|{message.chat.id}',
                                 senderId=f'Telegram|User|{message.from_user.id}',
                                 targetFrom=f'Telegram|{message.chat.type}',
                                 senderFrom='Telegram|User', senderName=message.from_user.username),
                         Session(message=message, target=message.chat.id, sender=message.from_user.id))
    await parser(msg)


async def on_startup(dispatcher):
    gather_list = []
    for x in Modules:
        if isinstance(Modules[x], Command) and Modules[x].autorun:
            gather_list.append(asyncio.ensure_future(Modules[x].function(FetchTarget)))
        if isinstance(Modules[x], Schedule):
            Scheduler.add_job(func=Modules[x].function, trigger=Modules[x].trigger, args=[FetchTarget])
    await asyncio.gather(*gather_list)
    Scheduler.start()
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
    await load_prompt(FetchTarget)


if dp:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
