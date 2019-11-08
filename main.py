import asyncio
import settings
from botroutine import bot

import logging
logger = logging.getLogger('bot')
from aiomysql.sa import create_engine


async def start():
    engine = await create_engine(read_default_file='bmstumap_admin/my.conf')
    try:
        await bot.loop(engine)
    except asyncio.CancelledError:
        pass


loop = asyncio.get_event_loop()

try:
    main_task = asyncio.ensure_future(start())
    loop.run_until_complete(main_task)
except KeyboardInterrupt:
    logger.debug("User cancelled")
    main_task.cancel()
    bot.stop()
finally:
    logger.debug("Closing loop")
    loop.stop()
    loop.close()
