from online_scrabble.bot.bot import BotError, ScrabbleBot


GAME_NAME = "game-two-bots"


if __name__ == "__main__":
    bot1 = ScrabbleBot("bot1")
    bot2 = ScrabbleBot("bot2 has a really long name really long name")

    bot1.join_game(GAME_NAME)
    bot2.join_game(GAME_NAME)

    bot1.start_game(GAME_NAME)

    while True:
        for bot in [bot1, bot2]:
            input("Press enter to continue...")
            bot.work(GAME_NAME)
