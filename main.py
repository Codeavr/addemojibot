import logging
from uuid import uuid4
from config import Config
import emoji_translate_api
import yandex_translate_api
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResult

config = Config()
ya_api = yandex_translate_api.API(config.API_KEY)
emoji_api = emoji_translate_api.API()

latin_chars = [chr(ch) for ch in range(ord('a'), ord('z') + 1)]


def all_chars_are_latin(text):
    for ch in text:
        if ch not in latin_chars and not ch.isidentifier() and not ch.isdigit() and not ch.isspace():
            return False
    return True


def on_inline_text(update, context):
    query = context.inline_query.query
    print('query:', query)
    update.inline_query.answer([InlineQueryResultArticle(
        id=uuid4(),
        title="Caps",
        input_message_content=query.upper())])

    return

    query = context.inline_query.query
    if all_chars_are_latin(query):
        eng_text = query
    else:
        eng_text = ya_api.translate_text(query)
    emojies = emoji_api.translate_to_emojies(eng_text)

    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            type='article',
            title="Translated",
            input_message_content=InputTextMessageContent(emojies))
    ]
    update.inline_query.answer(results)


def start(update, context):
    print('hi')
    update.message.reply_text('Hi!')


def create_updater(tg_token, proxy=None):
    if proxy is not None:
        return Updater(token=tg_token, request_kwargs={
            'proxy_url': proxy
        })
    else:
        return Updater(token=tg_token)


if __name__ == "__main__":
    updater = create_updater(config.TG_TOKEN, config.PROXY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(InlineQueryHandler(on_inline_text))
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    updater.start_polling()
    updater.idle()
