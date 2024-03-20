from telebot import TeleBot, types, apihelper
from time import sleep
from datetime import datetime, timedelta
from parsers import parser_base, kufar_parser, infoflat_parser


TOKEN = "7189321535:AAGFaQuc_4JnG_Lm7VH7ObM7zikJ3A1wPKs"
CHAT = 484336401
SLEEP_TIME_MINUTES = 5

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    print(message.chat)

    bot.send_message("I'm not ready")


def send_flats(flats: list[parser_base.FlatInfo]):
    for flat in flats:
        try:
            bot.send_photo(
                CHAT,
                flat.image,
                caption=flat.format_caption(),
                parse_mode="markdown"
            )
        except apihelper.ApiTelegramException as e:
            try:
                bot.send_message(CHAT, flat.format_caption(),
                                 parse_mode="markdown")
            except apihelper.ApiTelegramException as e:
                print(f"{e.description} -- {flat.url}")


def main():
    # bot.infinity_polling()

    kufar = parser_base.FlatParser(
        kufar_parser.KufarParserEngine, kufar_parser.URL)
    infoflat = parser_base.FlatParser(
        infoflat_parser.InfoflatParserEngine, infoflat_parser.URL)

    deltatime = timedelta(minutes=SLEEP_TIME_MINUTES + 2)

    while True:
        flats = infoflat.parse(deltatime) + kufar.parse(deltatime)

        print(f"{datetime.now()} -- {len(flats)}")
        send_flats(flats)

        sleep(SLEEP_TIME_MINUTES * 60)


if __name__ == '__main__':
    print("Hello from infoflatbyBot")

    # bot.send_message(CHAT, "Hello from infoflatbyBot")

    main()
