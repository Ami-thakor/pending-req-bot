import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserChannelsTooMuch, InputUserDeactivated
from pyrogram.types import Message


BOT_TOKEN = os.environ.get('BOT_TOKEN',
                           '5841283031:AAF6jf0KLG64Jjh9fPt4qn1HQ8IFCCq5arQ')

API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'
USER_SESSION = """BQDQj9UAuxRTqRtEX87rh7vSCsn0lcfjL9qMDUeCNmvynGEhegX1s4ft1LDTMyQGt8v4o99H8-5ZsTRS3bsUoeZ2ho47sPchse7tPBKTGIuUWqGxt9LVgU8vPhGA8xrdo9s50XGVLkJ6T0gGPQqAOs4EzrX73d1LayO42kT4otzOiqTCXEbM66yAuvtYH15GmrC7xe33ClZkK6ub-hjZp4Fw4BSj7QUdaOSlPlhrn7ZGOI3gkwp5ozHLY_e3YeEymmcckGRZyTXlvD91gkfEM0Pi9qfnf0b16kCOQTqry6HUVIRb53dlC9s58745uS0P8kBVMWqs8gJZ1pRATvB1alru_OfXFwAAAAFuk3J6AA"""


app = Client("ApprovalReqBot", api_id=API_ID,
             api_hash=API_HASH, session_string=USER_SESSION)


@app.on_message(filters.private & filters.command(['start']))
async def start_command(_, msg: Message):
    await msg.reply_text("Hello")


@app.on_message(filters.private & filters.command(['accept']))
async def approve_requests(_, msg: Message):
    try:
        chat_id = int(msg.text.split("/accept ")[-1])
    except:
        return
    edit_msg = await msg.reply_text('Started to Approving...Please dont send again this command until i complete this task..')
    s_count = 1
    u_count = 0
    try:

        async for user in app.get_chat_join_requests(chat_id):

            if s_count % 200 == 0:
                try:
                    await edit_msg.edit_text(
                        f"In Progress\n\n**Success:** {str(s_count)}\n**Failed:** {str(u_count)}"
                    )

                except:
                    pass

            if s_count % 1000 == 0:
                try:
                    await edit_msg.edit_text(
                        f"Sleeping for 30 seconds to avoid spam\n\n**Success:** {str(s_count)}\n**Failed:** {str(u_count)}"
                    )
                    await asyncio.sleep(30)
                    await edit_msg.edit_text(
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

        try:
            await edit_msg.edit_text(f"Completed\n\nSuccess: {s_count}\nUnsuccess: {u_count}")
        except:
            pass

    except:
        return


print("bot statfed")
app.run()
