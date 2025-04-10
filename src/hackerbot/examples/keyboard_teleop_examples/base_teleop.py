################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script is an example of how to use the base teleop behavior.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import hackerbot_helper as hhp
import time
import os

import sys, termios, atexit
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

class BaseTeleop:
    def __init__(self):
        self.kb = KBHit()

        self.robot = hhp.ProgrammedController()
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        self.robot.leave_base()
        self.robot.get_ping() 
        
        # Modify movement parameters
        self.step_size = 0.2 # mm
        self.max_l_step_size = 300.0 # mm/s
        self.max_r_step_size = 90.0 # degree/s

        self.stop = False
        self.last_key = None  # Track last keypress
        
        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def print_terminal_instructions(self):
        """Print instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n" + "="*10 + " Robot Teleop Controls " + "="*10 + "\r")
        print("\nMoving controls:\r")
        print("   ↑ / ↓    : forward/backward |   ← / →    : rotate left/right | space  : stop\r")
        print("o/p : increase/decrease step size by 10%\r")
        print("\nCTRL-C or '0' to quit\r")
        print("=" * 43 + "\r")

    def update_display(self):
        """Update step size in place without adding new lines"""
        sys.stdout.write(f"\rCurrent step size: {self.step_size:.2f}m\r")
        sys.stdout.flush()  # Ensure immediate update

    def get_command(self):
        key = None
        # Read keyboard input
        if self.kb.kbhit() is not None:
            key = self.kb.getch()
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
                sys.stdin.read(1)

            if key == self.last_key:
                self.last_key = None
                return None, None  

            self.last_key = key  # Update last key

            # Check for quit conditions
            if key == '0':  # '0' key to quit
                self.stop = True
                return None, None
                
            if key == 'o':
                self.step_size += 0.1
            elif key == 'p':
                self.step_size -= 0.1
            if key in ['\x1b[A', '\x1b[B', '\x1b[D', '\x1b[C', ' ']:
                l_vel, r_vel = self.get_base_command_from_key(key)
            else:
                l_vel = None
                r_vel = None
                
            return l_vel, r_vel
        else:
            self.last_key = None
            return 0.0, 0.0

    def get_base_command_from_key(self, key):
        if key == '\x1b[A':  # Up arrow - Forward
            l_vel = self.max_l_step_size * self.step_size
            r_vel = 0.0
        elif key == '\x1b[B':  # Down arrow - Backward
            l_vel = -self.max_l_step_size * self.step_size
            r_vel = 0.0
        elif key == '\x1b[D':  # Left arrow - Rotate left
            l_vel = 0.0
            r_vel = self.max_r_step_size * self.step_size
        elif key == '\x1b[C':  # Right arrow - Rotate right
            l_vel = 0.0
            r_vel = -self.max_r_step_size * self.step_size
        elif key == ' ':  # Space - Stop
            l_vel = 0.0
            r_vel = 0.0
        else:
            l_vel = None
            r_vel = None
        return l_vel, r_vel

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
            self.update_display()
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


# Main entry point
if __name__ == '__main__':
    teleop = None
    try:
        teleop = BaseTeleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()