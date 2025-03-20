import hackerbot_helper as hhp
import time
import math
import os

import sys, tty, termios, atexit
from select import select

class KBHit:
  
  def __init__(self):
    '''Creates a KBHit object that you can call to do various keyboard things.
    '''
    # Save the terminal settings
    self.fd = sys.stdin.fileno()
    self.new_term = termios.tcgetattr(self.fd)
    self.old_term = termios.tcgetattr(self.fd)

    # New terminal setting unbuffered
    self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

    # Support normal-terminal reset at exit
    atexit.register(self.set_normal_term)


  def set_normal_term(self):
    ''' Resets to normal terminal.  On Windows this is a no-op.
    '''
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


  def getch(self):
    ''' Returns a keyboard character after kbhit() has been called.
    '''
    ch1 = sys.stdin.read(1)
    if ch1 == '\x1b':
      # special key pressed
      ch2 = sys.stdin.read(1)
      ch3 = sys.stdin.read(1)
      ch = ch1 + ch2 + ch3
    else:
      # not a special key
      ch = ch1
    while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
        sys.stdin.read(1)
    return ch


  def kbhit(self):
    ''' Returns True if keyboard character was hit, False otherwise.
    '''
    dr,dw,de = select([sys.stdin], [], [], 0)
    while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
        sys.stdin.read(1)
    return dr != []

class Teleop:
    def __init__(self):
        self.kb = KBHit()

        self.robot = hhp.ProgrammedController()
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        self.robot.leave_base()
        
        # Modify movement parameters
        self.step_size = 0.2 # mm
        self.max_l_step_size = 300.0 # mm/s
        self.max_r_step_size = 90.0 # degree/s

        self.stop = False
        self.last_key = None  # Track last keypress
        
        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Restore terminal settings
            self.kb.set_normal_term()
            # Dock the robot
            self.robot.dock()
            time.sleep(2) 
            # Destroy the robot connection
            self.robot.destroy()
            
        except Exception as e:
            print(f"\nError during cleanup: {e}")
            # Try to restore terminal settings even if there's an error
            try:
                self.kb.set_normal_term()
            except:
                pass

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        self.cleanup()

    def print_terminal_instructions(self):
        """Print instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n=== Robot Teleop Controls ===\r")
        print("\nMoving controls:\r")
        print("   w    : forward\r")
        print("   a    : rotate left\r")
        print("   s    : stop\r")
        print("   d    : rotate right\r")
        print("   x    : backward\r")
        print("r/t : increase/decrease step size by 10%\r")
        print("\nCTRL-C/q to quit\r")
        print(f"\nCurrent step size: {self.step_size:.2f}m\r")
        print("=" * 30 + "\r")

    def get_command(self):
        key = None
        # Read keyboard input
        if self.kb.kbhit() is not None:
            key = self.kb.getch()
            # print(f"key: {key}\r")
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
                sys.stdin.read(1)

            if key == self.last_key:
                self.last_key = None
                return None, None  

            self.last_key = key  # Update last key

            # Check for quit conditions
            if key in ['q', 'Q']:  # Check for 'q' or Ctrl-C
                self.stop = True
                return None, None
                
            if key == 'r':
                self.step_size += 0.1
            elif key == 't':
                self.step_size -= 0.1

            if key == 'w':  # Forward
                l_vel = self.max_l_step_size * self.step_size
                r_vel = 0.0
            elif key == 'x':  # Backward
                l_vel = -self.max_l_step_size * self.step_size
                r_vel = 0.0
            elif key == 'a':  # Rotate left
                l_vel = 0.0
                r_vel = self.max_r_step_size * self.step_size
            elif key == 'd':  # Rotate right
                l_vel = 0.0
                r_vel = -self.max_r_step_size * self.step_size
            elif key == 's':  # Stop
                l_vel = 0.0
                r_vel = 0.0
            else:
                l_vel = None
                r_vel = None
            
            return l_vel, r_vel
        else:
            self.last_key = None
            return 0.0, 0.0

    def run(self):
        while not self.stop:
            l_vel, r_vel = self.get_command()
            if l_vel is not None and r_vel is not None:
                respone = self.robot.move(l_vel, r_vel)
                if respone == False:
                    break
                # print(f"l_vel: {l_vel}, r_vel: {r_vel}\r")
            l_vel = None
            r_vel = None
            time.sleep(0.01)


# Main entry point
if __name__ == '__main__':
    teleop = None
    try:
        teleop = Teleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()