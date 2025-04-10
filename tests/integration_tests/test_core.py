from hackerbot import Hackerbot

def main():
    try:
        bot = Hackerbot(verbose_mode=True) # Automatically called ping
        print(bot.core.ping())
        print(bot.core.versions())


    except Exception as e:
        print(e)
    finally:
        bot.destroy()

if __name__ == "__main__":
    main()