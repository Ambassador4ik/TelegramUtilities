from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import exceptions
from data import config
from translate.yandex import YandexTranslator
from voice.yandex import YandexVoiceGen
from fun import china, balaboba


# TODO: Save variables to config
app = Client("my_account", config.telegram_app_id, config.telegram_app_hash)

# Translation module
# Uses Yandex Cloud Translate API
# TODO: command setting from config, add Google Translate
TRANSLATION_ENABLED = False
TRANSLATION_LANG = "en"
translator = YandexTranslator()


@app.on_message(filters.regex('^' + config.command_trigger + "translate") & filters.me)
async def translate(client, message):
    global app
    global TRANSLATION_ENABLED
    global TRANSLATION_LANG
    if TRANSLATION_ENABLED:
        if len(message.text.split()) == 1:
            TRANSLATION_ENABLED = False
        else:
            TRANSLATION_LANG = message.text.split()[1]
    else:
        if len(message.text.split()) == 1:
            TRANSLATION_ENABLED = True
        else:
            TRANSLATION_ENABLED = True
            TRANSLATION_LANG = message.text.split()[1]
    await app.delete_messages(message.chat.id, message.id)


async def translate_func(_, __, ___):
    global TRANSLATION_ENABLED
    return TRANSLATION_ENABLED

translation_filter = filters.create(translate_func)


@app.on_message(translation_filter & filters.me)
async def translate(client, message):
    global app
    global TRANSLATION_LANG
    try:
        await app.edit_message_text(message.chat.id, message.id, translator.translate(message.text, TRANSLATION_LANG))
    except exceptions.bad_request_400.MessageNotModified:
        pass

# Voice Generation module
# Uses Yandex Cloud SpeechKit
# TODO: Add voice choise, add gTTS support, get rid of additional libs
voice_gen = YandexVoiceGen()


@app.on_message(filters.regex(config.command_trigger + "tts") & filters.me)
async def text_to_speach(client, message):
    global voice_gen
    voice_gen.gen_voice(message.text[5:])
    await app.delete_messages(message.chat.id, message.id)
    await app.send_voice(message.chat.id, "voice/temp/out.ogg")

# Debug chat module
# TODO: Add debug console functions
DEBUG_CHAT_ID = ""


@app.on_message(filters.regex(config.debug_trigger + "setdebug") & filters.me)
async def set_debug_chat(client, message):
    global DEBUG_CHAT_ID
    global app
    DEBUG_CHAT_ID = message.chat.id
    print(DEBUG_CHAT_ID)
    await app.send_message(DEBUG_CHAT_ID, "Debug chat set to this chat.")

# Fun module #1
# Sends reaction to all meseges in a selected chat
# TODO: Emoji choice, multiple choice
CLOWNADE_CHATS = []


@app.on_message(filters.regex(config.command_trigger + "clownade") & filters.me)
async def clownade_setter(client, message):
    global CLOWNADE_CHATS
    if message.chat.id not in CLOWNADE_CHATS:
        CLOWNADE_CHATS.append(message.chat.id)
    else:
        CLOWNADE_CHATS.remove(message.chat.id)
    await app.delete_messages(message.chat.id, message.id)


async def func1(_, __, ___):
    global CLOWNADE_CHATS
    return len(CLOWNADE_CHATS) > 0

clownade_filter = filters.create(func1)


@app.on_message((filters.incoming & clownade_filter))
async def clownade(client, message):
    global CLOWNADE_CHATS
    if message.chat.id in CLOWNADE_CHATS:
        await app.send_reaction(message.chat.id, message.id, emoji='🤡')

# Fun module #2
# Generates random shit in russian
# TODO: Add multiple creation


@app.on_message(filters.regex(config.command_trigger + "fresko") & filters.me)
async def say_smart_thing(client, message):
    await app.delete_messages(message.chat.id, message.id)
    await app.send_message(message.chat.id, china.wise_thing())

# Fun module #3
# Continues your messages using Balaboba


@app.on_message(filters.regex(config.command_trigger + "bala") & filters.me)
async def continue_message(client, message):
    resp = await balaboba.bala(message.text[6:])
    await app.edit_message_text(message.chat.id, message.id, resp)

app.run()
