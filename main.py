import logging
from uuid import uuid4
from config import Config
import emoji_translate_api
import yandex_translate_api
from telegram.ext import Filters, Updater, InlineQueryHandler, CommandHandler, MessageHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResult

config = Config()
ya_api = yandex_translate_api.API(config.API_KEY)
emoji_api = emoji_translate_api.API()

latin_chars = [chr(ch) for ch in range(ord('a'), ord('z') + 1)]


def all_chars_are_latin(text):
    for ch in text:
        if ch not in latin_chars and (ch.isidentifier() or ch.isdigit() or ch.isspace()):
            return False
    return True


def emojify(text) -> str:
    if text.strip() == '':
        return
    if all_chars_are_latin(text):
        eng_text = text
    else:
        eng_text = ya_api.translate_text(text)
    emojies = emoji_api.translate_to_emojies(eng_text)
    return emojies


def on_inline_text(bot, update):
    query = update.inline_query.query
    emojies = emojify(query)
    if emojies is None:
        return
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            type='article',
            title=emojies,
            input_message_content=InputTextMessageContent(emojies))
    ]
    update.inline_query.answer(results)


def start(bot, update):
    update.message.reply_text('Type any text to add some emojies to it')


def on_text_got(bot, update):
    update.message.reply_text(emojify(update.message.text))


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
    dispatcher.add_handler(MessageHandler(Filters.text, on_text_got))

    dispatcher.add_handler(InlineQueryHandler(on_inline_text))
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater.start_polling()
    updater.idle()
