import logging, os, random
import asyncio

from pyrogram import filters, enums, Client, __version__ as pyro_version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultAnimation, CallbackQuery

import requests

log = logging.getLogger(__name__)


# enable logging
FORMAT = f"[NekosBestBot] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'), logging.StreamHandler()], format=FORMAT)



API_ID = os.environ.get("API_ID", 29593257)
API_HASH = os.environ.get("API_HASH", "e9a3897c961f8dce2a0a88ab8d3dd843")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7106418611:sjsjkskekek")
SUPPORT = os.environ.get("SUPPORT", "NandhaSupport")
UPDATES = os.environ.get("UPDATES", "NandhaBots")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "NekosBestBot") 
BOT_URL = f"https://t.me/{BOT_USERNAME}"
PORT = int(os.environ.get("PORT", 8080))
BIND_ADDRESS = str(os.environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))



bot = Client(
  name="nekosbest",
  api_id=int(API_ID),
  api_hash=API_HASH,
  bot_token=BOT_TOKEN
)


buttons = [[
            InlineKeyboardButton("➕ Add Me To Group ➕", url=f"t.me/{BOT_USERNAME}?startgroup"),
],[

            InlineKeyboardButton("🆘 Help Plugin", callback_data="help_back"),
            InlineKeyboardButton("✨ Try Inline", switch_inline_query_current_chat=""),

],[
            InlineKeyboardButton("👥 Support", url=f"https://t.me/{SUPPORT}"),
            InlineKeyboardButton("📢 Updates", url=f"https://t.me/{UPDATES}")]]



PM_START_TEXT = """
**Welcome** {}~kun ฅ(≈>ܫ<≈)
`I'm A Neko Themed Telegram Bot Using Nekos.best! `
**Make Your Groups Active By Adding Me There! ××**
"""




####################################################################################################

# some funny entertainment plugins

@bot.on_message(filters.command("meme"))
async def meme(_, message):
      response = requests.get("https://nandhabots-api.vercel.app/meme")
      if response.status_code == 200:
           response_json = response.json()
           caption = response_json["title"]
           photo = response_json["image"]
           meme_id = response_json["meme_id"]
           return await message.reply_photo(
                photo=photo,
                caption=f"**{caption}** — `{meme_id}`")
      else:
         return await m.reply("🙀 Error...")



####################################################################################################

# developer plugins

import sys
import io
import time
import os
import subprocess
import traceback
import pyrogram as pyro

async def aexec(code, bot, message, my, m, r, ru):
    exec(
        "async def __aexec(bot, message, my, m, r, ru): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](bot, message, my, m, r, ru)



def p(*args, **kwargs):
    print(*args, **kwargs)


@bot.on_message(filters.command('sh') & filters.user([5696053228]))
async def shell_command(bot, message):
     if len(message.text.split()) < 2:
         return await message.reply("🤔 Shell command to execute??")
     command = message.text.split(maxsplit=1)[1]

     msg = await message.reply("**--> Shell command processing....**", quote=True)
     shell_output = subprocess.getoutput(command)

     if len(shell_output) > 4000:
          with open("shell.txt", "w+") as file: 
               file.write(shell_output)
          await msg.delete()
          await message.reply_document(
              document="shell.txt",
              quote=True
          )
          os.remove("shell.txt"); return
     else:
         await msg.edit_text(f"```py \n{shell_output}```")




@bot.on_message(filters.command('e') & filters.user([5696053228]))
async def evaluate(bot, message):

    status_message = await message.reply("`Running Code...`")
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    start_time = time.time()

    r = message.reply_to_message        
    m = message
    my = getattr(message, 'from_user', None)
    ru = getattr(r, 'from_user', None)

    if r:
        reply_to_id = r.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(
                   code=cmd, 
             message=message,
             my=my,
                m=message, 
                r=r,
                ru=ru,
                bot=bot
        )
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    taken_time = round((time.time() - start_time), 3)
    output = evaluation.strip()
    format_text = "<pre>Command:</pre><pre language='python'>{}</pre> \n<pre>Takem Time: {}'s:</pre><pre language='python'> {}</pre>"
    final_output = format_text.format(cmd, taken_time, output)

    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=f'`{cmd}`',
            quote=True,

        )
        os.remove(filename)
        await status_message.delete()
        return
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.HTML)
        return 



####################################################################################################




####################################################################################################

#inline for @nekosBestBot


NEKOS_BEST = {"neko":{"format":"png"},"waifu":{"format":"png"},"husbando":{"format":"png"},"kitsune":{"format":"png"},"lurk":{"format":"gif"},"shoot":{"format":"gif"},"sleep":{"format":"gif"},"shrug":{"format":"gif"},"stare":{"format":"gif"},"wave":{"format":"gif"},"poke":{"format":"gif"},"smile":{"format":"gif"},"peck":{"format":"gif"},"wink":{"format":"gif"},"blush":{"format":"gif"},"smug":{"format":"gif"},"tickle":{"format":"gif"},"yeet":{"format":"gif"},"think":{"format":"gif"},"highfive":{"format":"gif"},"feed":{"format":"gif"},"bite":{"format":"gif"},"bored":{"format":"gif"},"nom":{"format":"gif"},"yawn":{"format":"gif"},"facepalm":{"format":"gif"},"cuddle":{"format":"gif"},"kick":{"format":"gif"},"happy":{"format":"gif"},"hug":{"format":"gif"},"baka":{"format":"gif"},"pat":{"format":"gif"},"nod":{"format":"gif"},"nope":{"format":"gif"},"kiss":{"format":"gif"},"dance":{"format":"gif"},"punch":{"format":"gif"},"handshake":{"format":"gif"},"slap":{"format":"gif"},"cry":{"format":"gif"},"pout":{"format":"gif"},"handhold":{"format":"gif"},"thumbsup":{"format":"gif"},"laugh":{"format":"gif"}}


NEKOS_BEST_TEXT = {
    "neko": [
        "nyaa~ {name} shows off their kawaii neko ears! 🐱✨",
        "meow meow~ {name} purrs and wiggles their tail~ 🐾💝",
        "nya nya~ {name} is feeling extra catlike today! 😺💫"
    ],
    "waifu": [
        "nyaaaa!~ {name} found their purrfect waifu! 😻💖",
        "meow meow~ {name}'s tail wiggles excitedly~ 🐱💕",
        "purr purr~ {name} nuzzles their waifu nya! ✨😽"
    ],
    "husbando": [
        "nyaaa!~ {name} found their dreamy husbando! 😻💝",
        "meow meow~ {name}'s ears perk up happily~ 🐱💗",
        "purrrr~ {name} circles around excitedly nya! 😸✨"
    ],
    "kitsune": [
        "nya nya~ {name} meets a foxy friend! 🦊💫",
        "meow!~ {name}'s tail dances with excitement~ 🐱✨",
        "nyaa!~ {name} shares mystic powers nya! 😺🌟"
    ],
    "happy": [
        "nyaaaa!~ {name} purrs with joy! 😸💝",
        "meow meow!~ {name}'s tail stands straight up! 🐱✨",
        "purr purr~ {name} rolls around happily nya! 😺💫"
    ],
    "lurk": [
        "nya...~ {name} stalks their prey quietly~ 🐱👀",
        "meow?~ {name} wiggles butt before pouncing~ 😼💫",
        "*silent pawsteps* {name} lurks nya... 😺✨"
    ],
    "shoot": [
        "nya nya!~ {name} pounces with precision! 😸⚡",
        "meow!~ {name} shows their hunting skills~ 🐱💫",
        "nyaa!~ {name} catches their target nya! 😺✨"
    ],
    "sleep": [
        "nyaaa~ {name} curls up for a catnap! 😴💤",
        "meow...~ {name} purrs softly in their sleep~ 🐱💫",
        "zzz~ {name} dreams of fish nya... 😺✨"
    ],
    "shrug": [
        "nya?~ {name} tilts head in confusion! 😸❓",
        "meow meow~ {name} flicks tail dismissively~ 🐱💫",
        "nyaa~ {name} doesn't know nya! 😺✨"
    ],
    "stare": [
        "nya!~ {name} watches with big kitty eyes! 👀✨",
        "meow~? {name}'s tail swishes curiously~ 🐱💫",
        "nyaa!~ {name} stares intently nya! 😺🔍"
    ],
    "wave": [
        "nya nya!~ {name} waves their paw! 🐱👋",
        "meow meow!~ {name} greets with tail up high~ 😺💫",
        "nyaa!~ {name} says hewwo nya! 😸✨"
    ],
    "poke": [
        "nya!~ {name} bats with their paw! 🐱🐾",
        "meow~! {name} taps curiously~ 😺💫",
        "nyaa!~ {name} pokes with beans nya! 😸✨"
    ],
    "smile": [
        "nya nya!~ {name} shows their fangs! 😺💝",
        "meow~! {name}'s whiskers twitch happily~ 🐱✨",
        "nyaa!~ {name} purrs with joy nya! 😸💫"
    ],
    "peck": [
        "nya~! {name} gives a kitty kiss! 😽💝",
        "meow~! {name} nuzzles sweetly~ 🐱✨",
        "nyaa!~ {name} shows affection nya! 😺💫"
    ],
    "wink": [
        "nya nya~! {name} winks playfully! 😺💫",
        "meow~! {name}'s tail curls mischievously~ 🐱✨",
        "nyaa!~ {name} is being sneaky nya! 😸💝"
    ],
    "blush": [
        "nya...~ {name}'s ears turn pink! 😳💝",
        "meow...~ {name} hides behind their paws~ 🐱✨",
        "nyaa!~ {name} blushes bright red nya! 😺💫"
    ],
    "smug": [
        "nya nya~! {name} looks very pleased! 😼✨",
        "meow~! {name}'s tail stands proud~ 🐱💫",
        "nyaa!~ {name} knows they're purrfect nya! 😺💝"
    ],
    "tickle": [
        "nya nya!~ {name} squirms and giggles! 😸✨",
        "meow!~ {name}'s tail poofs up~ 🐱💫",
        "nyaa!~ {name} can't stop laughing nya! 😺💝"
    ],
    "yeet": [
        "nya!~ {name} pounces far away! 😸💨",
        "meow!~ {name} zooms at light speed~ 🐱✨",
        "nyaa!~ {name} leaps into space nya! 😺💫"
    ],
    "think": [
        "nya?~ {name} ponders deeply! 🐱💭",
        "meow...~ {name}'s tail twitches in thought~ 😺✨",
        "nyaa!~ {name} has an idea nya! 😸💫"
    ],
    "highfive": [
        "nya nya!~ {name} raises their paw high! 🐾✨",
        "meow!~ {name} gives pawfive~ 🐱💫",
        "nyaa!~ {name} celebrates nya! 😺💝"
    ],
    "feed": [
        "nya nya!~ {name} noms delicious food! 😋🐱",
        "meow!~ {name} munches happily~ 😺🍱",
        "nyaa!~ {name} enjoys treats nya! 🐱💝"
    ],
    "bite": [
        "nya!~ {name} nomps gently! 🐱💫",
        "meow!~ {name} shows their fangs~ 😺✨",
        "nyaa!~ {name} takes a nibble nya! 😸🐾"
    ],
    "bored": [
        "nya...~ {name} needs attention! 😿💫",
        "meow...~ {name}'s tail droops sadly~ 🐱✨",
        "nyaa...~ {name} has nothing to do nya... 😺💤"
    ],
    "nom": [
        "nya nya!~ {name} enjoys their meal! 😋🐱",
        "meow!~ {name} munches fishies~ 😺🐟",
        "nyaa!~ {name} gobbles treats nya! 🐱💝"
    ],
    "yawn": [
        "nyaaa~! {name} shows their fangs! 😺💤",
        "meow...~ {name} needs a catnap~ 🐱✨",
        "nyaa...~ {name} is sleepy nya... 😪💫"
    ],
    "facepalm": [
        "nya...~ {name} covers face with paw! 🐱💫",
        "meow...~ {name}'s ears droop in disbelief~ 😿✨",
        "nyaa...~ {name} can't believe it nya... 😺🤦"
    ],
    "cuddle": [
        "nya nya!~ {name} snuggles close! 🐱💝",
        "meow~! {name} purrs contentedly~ 😺💫",
        "nyaa!~ {name} wants warmth nya! 😸✨"
    ],
    "kick": [
        "nya!~ {name} uses back paws! 🐱⚡",
        "meow!~ {name} shows ninja kicks~ 😺💫",
        "nyaa!~ {name} is strong nya! 😸✨"
    ],
    "hug": [
        "nya nya!~ {name} gives warm hugs! 🐱💝",
        "meow~! {name} wraps tail around~ 😺💫",
        "nyaa!~ {name} snuggles tight nya! 😸✨"
    ],
    "baka": [
        "nya!~ {name} swishes tail angrily! 😾💢",
        "meow!~ {name}'s fur stands up~ 🐱⚡",
        "nyaa!~ {name} is annoyed nya! 😺✨"
    ],
    "pat": [
        "nya~! {name} enjoys the pets! 🐱💝",
        "meow~! {name} purrs happily~ 😺✨",
        "nyaa!~ {name} leans into pats nya! 😸💫"
    ],
    "nod": [
        "nya!~ {name} bobs head in agreement! 🐱✨",
        "meow~! {name}'s ears wiggle~ 😺💫",
        "nyaa!~ {name} understands nya! 😸💝"
    ],
    "nope": [
        "nya!~ {name} turns their nose up! 😾💢",
        "meow!~ {name}'s tail says no~ 🐱✨",
        "nyaa!~ {name} refuses nya! 😺💫"
    ],
    "kiss": [
        "nya~! {name} gives nose boops! 😽💝",
        "meow~! {name} shows affection~ 🐱✨",
        "nyaa!~ {name} gives kisses nya! 😺💫"
    ],
    "dance": [
        "nya nya!~ {name} moves their paws! 🐱💃",
        "meow~! {name}'s tail dances~ 😺✨",
        "nyaa!~ {name} grooves nya! 😸💫"
    ],
    "punch": [
        "nya!~ {name} swats with paw! 🐱⚡",
        "meow!~ {name} shows their strength~ 😺💫",
        "nyaa!~ {name} is powerful nya! 😸✨"
    ],
    "handshake": [
        "nya!~ {name} offers their paw! 🐱🤝",
        "meow~! {name} greets formally~ 😺✨",
        "nyaa!~ {name} makes friends nya! 😸💫"
    ],
    "slap": [
        "nya!~ {name} swats with beans! 🐱⚡",
        "meow!~ {name}'s paw goes swoosh~ 😺💫",
        "nyaa!~ {name} is upset nya! 😾✨"
    ],
    "cry": [
        "nya...~ {name} needs comfort! 😿💧",
        "meow...~ {name}'s ears droop sadly~ 🐱💫",
        "nyaa...~ {name} is sad nya... 😺✨"
    ],
    "pout": [
        "nya!~ {name} puffs their cheeks! 😾💢",
        "meow!~ {name}'s tail twitches angrily~ 🐱✨",
        "nyaa!~ {name} is grumpy nya! 😺💫"
    ],
    "handhold": [
        "nya~! {name} offers their paw! 🐱💝",
        "meow~! {name} wants to hold paws~ 😺✨",
        "nyaa!~ {name} stays close nya! 😸💫"
    ],
    "thumbsup": [
        "nya!~ {name} raises their paw! 🐱👍",
        "meow~! {name} approves happily~ 😺💫",
        "nyaa!~ {name} says yes nya! 😸✨"
    ],
    "laugh": [
        "nya nya!~ {name} can't stop giggling! 😸💫",
        "meow~! {name} purrs with laughter~ 🐱✨",
        "nyaa!~ {name} is happy nya! 😺💝"
    ]
}


def get_InputMediaType(data):
       format = data['format']

       if format == "png":
            return InlineQueryResultPhoto
       elif format == "gif":
            return InlineQueryResultAnimation

       raise Exception(f'Unkown media type found for get_InputMediaType: {format}')




def convert_button(data, columns):
    result = []

    for i in range(0, len(data), columns):
        result.append(data[i:i + columns])

    # If the last row has fewer columns and there are still data left, create a new row
    if len(result[-1]) < columns and len(data) > len(result[-1]) + columns:
        new_row = data[len(result[-1]) + columns:]
        result.append(new_row)

    return result


NEKOS_BUTTONS = convert_button(
    [InlineKeyboardButton(text=q, switch_inline_query_current_chat=q) for q in list(NEKOS_BEST)],
    columns=4
)

@bot.on_inline_query()
async def inline(bot, query):
    q = query.query
    user = query.from_user
    inline_query_id = query.id

    if not q:
        results = [
            InlineQueryResultArticle(
                title="Query Not Found! 😹",
                input_message_content=InputTextMessageContent(message_text="**Query nyan found! I needed an endpoint, senpai~!** 🐾"),
                reply_markup=InlineKeyboardMarkup(NEKOS_BUTTONS)
            )
        ]
        return await bot.answer_inline_query(inline_query_id, results)

    pattern = q.split()[0].lower()
    src = NEKOS_BEST.get(pattern)
    if not src:
        results = [
            InlineQueryResultArticle(
                title="Given nyan! Query Not Found! 😹",
                input_message_content=InputTextMessageContent(message_text="❌ **Given nyan query is not found! Please use a valid endpoint, senpai~!** 😸"),
                reply_markup=InlineKeyboardMarkup(NEKOS_BUTTONS)
            )
        ]
        return await bot.answer_inline_query(inline_query_id, results)

    results = []
    api_url = f"https://nekos.best/api/v2/{pattern}?amount=20"
    api_result = requests.get(api_url).json()
    data_result = api_result['results']
    media_type = get_InputMediaType(src)
    for data in data_result:
        results.append(
            media_type(
                data['url'],
                caption=f"**{random.choice(NEKOS_BEST_TEXT[pattern]).format(name=user.full_name)}**",
            )
        )
    return await bot.answer_inline_query(inline_query_id, results, cache_time=2, is_gallery=True)




####################################################################################################


@bot.on_message(filters.command(["start","help"]))
async def start(_, m):
       url = "https://nekos.best/api/v2/neko"
       r = requests.get(url)
       e = r.json()
       NEKO_IMG = e["results"][0]["url"]
       await m.reply_photo(photo=NEKO_IMG,caption=PM_START_TEXT.format(m.from_user.mention),
             reply_markup=InlineKeyboardMarkup(buttons))

HELP_TEXT = """
**Anime Themed SFW:**
• Kiss : /kiss To Kiss A Person
• Highfive : /highfive To Highfive A Person
• Happy : /happy To Makes A Person Happy
• Laugh : /laugh To Makes A Person Laugh
• Bite : /bite To Bite A Person
• Poke : /poke To Poke A Person
• Tickle : /tickle To Tickle A Person
• Wave : /wave To Wave A Person
• Thumbsup : /thumbsup To Thumbsup A Person
• Stare : /stare To Makes A Person Stare
• Cuddle : /cuddle To Cuddle A Person
• Smile : /smile To Makes A Person Smile
• Baka : /baka To Say A Person Baka
• Blush : /blush To Makes A Person Blush

✨ **Press 'More' for know more commands.**
"""

@bot.on_callback_query(filters.regex("help_back"))
async def helpback(_, query: CallbackQuery):
           query = query.message
           await query.edit_caption(HELP_TEXT,
             reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("More", callback_data="more_help_text"),
                InlineKeyboardButton("Info", callback_data="about_back")]]))

ABOUT_TEXT = """
**Hello Dear Users!**
`I'm A Neko Themed Telegram Bot Using Nekos.best! `

**My Pyro version**: `{}`
**My Updates**: @NandhaBots
**My Support**: @NandhaSupport

⚡ **Source**: 
https://github.com/NandhaXD/nekosBestBot
"""

@bot.on_callback_query(filters.regex("about_back"))
async def about(_, query: CallbackQuery):
           query = query.message
           await query.edit_caption(ABOUT_TEXT.format(str(pyro_version)),
             reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Back", callback_data="help_back")]]))

MORE_HELP_TEXT = """
**Anime themed SFW:**
• Think : /think To Makes A Person Think
• Pout : /pout To Makes A Person Pout
• Facepalm : /facepalm To Makes A Person Facepalm
• Wink : /wink To Makes A Person Wink
• Smug : /smug To Makes A Person Smug
• Cry : /cry To Makes A Person Cry
• Dance : /dance To Makes A Person Dance
• Feed : /feed To Feed A Person
• Shrug : /shrug To Shrug A Person
• Bored : /bored To Makes A Person Bored
• Pat : /pat To Pat A Person
• Hug : /hug To Hug A Person
• Slap : /slap To Slap A Person
• Cute : /cute To Say Me Cute
• Waifu : /waifu To Send Random Waifu Image
• Kitsune : /kitsune To Send Random Kitsune Image
• Sleep : /sleep To Say I Am G
