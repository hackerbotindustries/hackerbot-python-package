from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        print("Looking")
        bot.head.look(180, 180, 100)
        



    except Exception as e:
        print(e)
    finally:
        time.sleep(5)
        bot.destroy()

if __name__ == "__main__":
    main()