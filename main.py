import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserChannelsTooMuch, InputUserDeactivated
from pyrogram.types import Message


BOT_TOKEN = os.environ.get('BOT_TOKEN',
                           '5841283031:AAF6jf0KLG64Jjh9fPt4qn1HQ8IFCCq5arQ')

API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'
USER_SESSION = """BQAOCfwkGWhIiohz0KTMfn3-dgIbdympSwjgZ7RmoP8lgEd55-eoy8S1NsWgVG_3_2AkFHVsLgBCUPgAYcJWncv4IcGMQEYQ23lJfTfzONnn7QtVDZHQH-YkZ2ySe3scUDaSKxVRTuoLivKPGKpSFLm63Fs0vw-4X42CVJi8AxDqPrwXUPnBKdKCfsiHH0o9tDxvzkj0ruyT0yHeSn75cjWDg0C57cqOG2ReREx4iMRTCzhk3pm1D-TVCAJUpBKK24vgnaL7dDGpgovFgjjur-X3svBX7IHYfYUc2SxNgAJNL3bSsqvmZZ0ub0d5dfFYMGDhPusLABYM_BC4v1AiaK9tAAAAAW6TcnoA"""


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
