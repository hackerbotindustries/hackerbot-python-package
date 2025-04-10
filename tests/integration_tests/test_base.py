from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        # bot.base.initialize()
        # bot.base.set_mode(2)
        # bot.base.status()
        # bot.base.position()
        # print("Starting")
        # bot.base.start()
        # bot.base.quickmap()
        # bot.base.kill()
        # bot.base.trigger_bump(True, True)
        # print("Driving")
        # bot.base.drive(-500, 0)
        # bot.base.drive(100, 0)
        # bot.base.drive(0, 360)
        for i in range(10):
            print("Driving")
            bot.base.drive(-500, 0)
            bot.base.drive(0, -180)
            bot.base.drive(100, 0)
            bot.base.drive(0, -180)
            bot.base.drive(100, 0)
            print("Docking")
            bot.base.dock()

    except Exception as e:
        print(e)
    finally:
        print("End")
        bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()