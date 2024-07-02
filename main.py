import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import (
    UserChannelsTooMuch,
    InputUserDeactivated,
    UserAlreadyParticipant,
)

from pyrogram.types import Message, ChatJoinRequest


BOT_TOKEN = os.environ.get(
    "BOT_TOKEN", "6308227197:AAHweeHPdwsa9SDWpr7g627qxpqtbZsaWsU"
)


API_ID = 22678379
API_HASH = "8c901dc52cf2cf336739713f37c6222c"
USER_SESSION = """AQFaC2sAIaW5YKlAT00hrs6u_5jN4t8b21K9TmELWPoBe_E3r4eU98m3bV46ghbHAacXbhNtM90drQuLfOFPt-4CyqXMtNEZ2uryZCiq1lCoTSaznrC40nGBP-LQjLLI_YSVo9M36_6QIdpT4d7qPcinln9W85HA2iWxOjT5ORVdyC2lhiKfU2q8Paww0lb1XyRK1Hd9T1Jt-RPOnBlTZcgbvUJUGPRk6ysYAOh_yDDLFRindrMtdgKMHeaaMp_XcAkx8fSbLSdBIGSxweFJwmnZFVEoT0ecCges-RgFj6ISFAqTFzCkN4ccRRHvl5RyUpDahnOxfxVCYn1x-eymnRohVarroQAAAAG0Q8N6AA"""

user_session = os.environ.get("USER_SESSION", USER_SESSION)
app = Client(
    "MayaApprovalReqBot", api_id=API_ID, api_hash=API_HASH, session_string=user_session
)
bot = Client("MayaRobot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.private & filters.regex("!start"))
async def start_command(_, msg: Message):
    await msg.reply_text("Hello from user.")


@bot.on_message(filters.private & filters.command(["start"]))
async def start_command_h(_, msg: Message):
    await msg.reply_text("Hello from bot")


@app.on_message(filters.private & filters.regex("!accept"))
async def approve_requests(_, msg: Message):
    print("triggerd userbot")
    try:
        chat_id = int(msg.text.split("!accept ")[-1])
    except:
        return
    sent_msg = await msg.reply_text(
        "Started to Accepting...Please don't send again this command until i complete this task.."
    )
    s_count = 1
    u_count = 0
    try:

        async for user in app.get_chat_join_requests(chat_id):

            if s_count % 400 == 0:
                try:
                    await sent_msg.edit_text(
                        f"In Progress\n\n**Accepted:** {str(s_count)}"
                    )

                except:
                    pass

            if s_count % 1000 == 0:
                try:
                    await sent_msg.edit_text(
                        f"Sleeping for 10 seconds to avoid spam\n\n**Accepted:** {str(s_count)}\n**Rejected:** {str(u_count)}"
                    )
                    await asyncio.sleep(10)
                    await sent_msg.edit_text(
                        f"In Progress\n\n**Success:** {str(s_count)}\n**Failed:** {str(u_count)}"
                    )

                except:
                    pass

            try:
                UserID = user.user.id
                await app.approve_chat_join_request(chat_id, UserID)
                s_count += 1
            except UserChannelsTooMuch:
                u_count += 1

            except InputUserDeactivated:
                u_count += 1

            except BaseException as E:
                u_count += 1
    except Exception as x:
        print(x)
        return

    try:
        await sent_msg.edit_text(
            f"Completed\n\nSuccess: {s_count}\nUnsuccess: {u_count}"
        )
    except:
        pass


@bot.on_chat_join_request()
async def reqs_handler(app: Client, request: ChatJoinRequest):

    print("trigger bot")
    chatid = request.chat.id
    user = request.from_user.id

    try:
        await app.approve_chat_join_request(chatid, user)
        await asyncio.sleep(1)

    except UserAlreadyParticipant:
        pass

    except UserChannelsTooMuch:
        pass

    except Exception as ex:
        print(ex)


print("bot started ;)")
bot.start()
app.run()
