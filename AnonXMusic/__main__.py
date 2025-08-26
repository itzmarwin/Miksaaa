import asyncio
import warnings
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils import monitor
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # Check assistant client variables
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    # Load sudo users
    await sudo()

    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # Start bot & userbot
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AnonXMusic.plugins." + all_module)
    LOGGER("AnonXMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Anony.start()

    # Decorators load
    await Anony.decorators()

    LOGGER("AnonXMusic").info(
        "AnonX Music Bot Started Successfully.\n\nDon't forget to visit @FallenAssociation"
    )

    # Start monitor & idle loop
    await monitor()
    await idle()

    # Stop clients on exit
    await app.stop()
    await userbot.stop()
    LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="There is no current event loop",
            category=DeprecationWarning,
        )
        asyncio.run(init())
