from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        for _ in range(100):
            bot.base.maps.goto(1, 1, 0, 0.5)
            bot.base.maps.goto(0.5, 1, 0, 0.5)
            bot.base.maps.goto(0.5, 0.5, 180, 0.5)
            bot.base.maps.goto(1, 0.5, 180, 0.5)


    except Exception as e:
        print(e)
    finally:
        bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()