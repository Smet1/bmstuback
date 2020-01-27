import json
import logging
import os

from aiotg import Chat

import settings
from proxybot import ProxyBot

log = logging.getLogger('bot')

bot = ProxyBot(api_token="592413955:AAHkMWMBu7tyt60I9DBqHtd0LUqAwkpYixg", proxy='socks5://188.166.100.226:1080')


def check_plan(filename):
    return _check(filename, 'python "bmstumap_admin/manage.py" plan')


def _check(filename, command):
    foutput = os.path.join('rendered', "{}.png".format(filename))
    if not os.path.isfile(foutput):
        finput = os.path.join('bmstumap_admin/paths', "{}.svg".format(filename))
        # OPTIMIZE: really heavy task can be better
        if not os.path.isfile(finput):
            os.system(command)

        os.system('svgexport "{}" "{}" pad {}'.format(finput, foutput, settings.OUTPUT_RESOLUTION))

    return foutput


def typing_status(func):
    async def wrapped(chat: Chat, match):
        await chat.send_chat_action('typing')
        await func(chat, match)

    return wrapped


@bot.command(r"(/help|помагите|помогите)")
@typing_status
async def echo(chat: Chat, match):
    help_text = """
    /help - для получения справки
    /proff ФИО - для получения текущего местоположения интересующей вас личности ха-ха-ха рефакторнуть
    еще можно написать "Где Гапанюк" и узнать
    /find откуда куда - для получения карты сокровищ ха-ха-ха рефакторнуть
    еще можно написать "как пройти от до"
    /where номер помещения - показать на карте нужный кабинет
    /all - общий план помещения
    eще можно написать "план"
    """.strip()
    return chat.send_text(help_text)


@bot.command(r"(/all|план|вид|общий план|здание)")
@typing_status
async def building_plan(chat: Chat, match):
    foutput = check_plan('bmstuplan_all')
    with open(foutput, 'rb') as file:
        await chat.send_photo(file)

    await asyncio.wait(0)


@bot.command(r"/where (.*)")
@typing_status
async def building_plan(chat: Chat, match):
    async with bot._db_conn.acquire() as conn:
        query = """
            SELECT *
            FROM cabinet
            WHERE cabinet.name='{}' and cabinet.auditoria='1'
            LIMIT 1;
        """.format(match.group(1))

        cabinet = await (await conn.execute(query)).fetchone()

        if cabinet:
            filename = 'bmstunode_{}'.format(cabinet.id)
            command = 'python "bmstumap_admin/manage.py" createnode {}'.format(cabinet.id)
            foutput = _check(filename, command)

            with open(foutput, 'rb') as file:
                await chat.send_photo(file)
            await asyncio.wait(0)

            return

    return chat.send_text('Я не знаю где находится {}'.format(match.group(1)))


@bot.command(r"(?i:/proff|где) (.*)")
@typing_status
async def get_proff(chat: Chat, match):
    async with bot._db_conn.acquire() as conn:
        query = """
            SELECT *
            FROM employee
            WHERE CONCAT(last_name,' ',first_name,' ',middle_name,' ') LIKE '%{0}%'
            LIMIT 10;
        """.format(match.group(1))

        result = await (await conn.execute(query)).fetchall()
        log.debug(result)
        if result and len(result) == 1:
            employee = result[0]
            schedule_query = """
                SELECT
                    cabinet.name,
                    schedule.time_from,
                    schedule.time_to
                FROM schedule
                JOIN cabinet ON schedule.cabinet_id=cabinet.id
                WHERE (curtime() between time_from and time_to)
                    and (weekday(curdate())=weekday)
                    and (employee_id='{}');
            """.format(employee.id)
            schedule = await (await conn.execute(schedule_query)).fetchone()
            log.debug(schedule)
            efio = "{} {} {}".format(employee.last_name, employee.first_name, employee.middle_name)
            if schedule:
                time_from = str(schedule.time_from)[:-3]
                time_to = str(schedule.time_to)[:-3]
                return chat.reply("{} сейчас({}-{}) в {}".format(efio, time_from, time_to, schedule.name))

            return chat.reply("Я не знаю, где сейчас {}".format(efio))

        if result and len(result) > 1:
            kb = {
                'type': 'InlineKeyboardMarkup',
                "inline_keyboard": list([
                    [{
                        'type': 'InlineKeyboardButton',
                        "text": "{} {} {}".format(i.last_name, i.first_name, i.middle_name),
                        "callback_data": "proff-{}".format(i.id)
                    }] for i in result
                ])
            }
            log.debug(kb)
            return chat.send_text('Уточните запрос', reply_markup=json.dumps(kb))

    return chat.reply("По вашему запросу ничего не найдено")


@bot.command(r"/find (\d+.*?) (\d+.*)")
@typing_status
async def find_path(chat: Chat, match):
    async with bot._db_conn.acquire() as conn:
        query = """
            SELECT *
            FROM cabinet
            WHERE cabinet.name='{}' AND cabinet.auditoria='1'
            LIMIT 1;
        """.format(match.group(1))

        start = await (await conn.execute(query)).fetchone()

        query = """
            SELECT *
            FROM cabinet
            WHERE cabinet.name='{}' AND cabinet.auditoria='1'
            LIMIT 1;
        """.format(match.group(2))

        end = await (await conn.execute(query)).fetchone()

    if not start:
        return chat.reply('Увы, я не знаю где находится {}'.format(match.group(1)))

    if not end:
        return chat.reply('Увы, я не знаю где находится {}'.format(match.group(2)))

    filename = 'bmstuplan_{}_to_{}'.format(start.id, end.id)
    command = 'python "bmstumap_admin/manage.py" createpath {} {}'.format(start.id, end.id)
    foutput = _check(filename, command)

    log.debug('sending file {}'.format(foutput))
    with open(foutput, 'rb') as file:
        await chat.send_photo(file)

    await asyncio.wait(0)


@bot.command(r"/pos (.*)")
@typing_status
async def posheldfind(chat: Chat, match):
    async with bot._db_conn.acquire() as conn:
        query = """
            SELECT
                position.name as position,
                first_name as fname,
                last_name as lname,
                middle_name as mname,
                time_from,
                time_to,
                cabinet.name as cabinet
            FROM posheld
                JOIN position ON position.id=posheld.position_id
                JOIN employee on employee.id=posheld.employee_id
                JOIN schedule on schedule.employee_id=posheld.employee_id
                JOIN cabinet on cabinet.id=schedule.cabinet_id
            WHERE position.name LIKE '%{}%'
            LIMIT 10;
        """.format(match.group(1))

        result = await (await conn.execute(query)).fetchall()
        log.debug(result)
        if result and len(result) == 1:
            ans = result[0]
            efio = "{} {} {}".format(ans.lname, ans.fname, ans.mname)
            return chat.reply('{} {} сейчас в {}'.format(ans.position, efio, ans.cabinet))

        return chat.reply('Уточните ваш запрос')
    return chat.reply('Извините, по вашему запросу ничего не найдено')


@bot.callback(r"proff-(\d+)")
async def proff_clarify(chat, cq, match):
    mid = cq.src['message']['message_id']
    async with bot._db_conn.acquire() as conn:
        query = """
            SELECT
                cabinet.name as cabinet,
                employee.first_name as fname,
                employee.last_name as lname,
                employee.middle_name as mname,
                schedule.time_from,
                schedule.time_to
            FROM schedule
                JOIN cabinet ON schedule.cabinet_id=cabinet.id
                JOIN employee ON employee.id=schedule.employee_id
            WHERE (curtime() between time_from and time_to)
                and (weekday(curdate())=weekday)
                and (employee_id='{}')
            LIMIT 1;
        """.format(match.group(1))

        ans = await (await conn.execute(query)).fetchone()
        log.debug(ans)
        if ans:
            efio = "{} {} {}".format(ans.lname, ans.fname, ans.mname)
            time_from = str(ans.time_from)[:-3]
            time_to = str(ans.time_to)[:-3]
            return chat.edit_text(mid, '{} сейчас({}-{}) в {}'.format(efio, time_from, time_to, ans.cabinet))

        query = """
            SELECT
                employee.first_name as fname,
                employee.last_name as lname,
                employee.middle_name as mname
            FROM employee
            WHERE employee.id='{}'
            LIMIT 1;
        """.format(match.group(1))

        ans = await (await conn.execute(query)).fetchone()

        if ans:
            efio = "{} {} {}".format(ans.lname, ans.fname, ans.mname)
            return chat.edit_text(mid, "Я не знаю, где сейчас {}".format(efio))

    return chat.edit_text(mid, 'Произошла какая-то ошибка, попробуйте снова')
