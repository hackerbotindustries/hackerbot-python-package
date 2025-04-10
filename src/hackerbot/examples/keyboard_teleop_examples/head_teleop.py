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
# This script is an example of how to use the head teleop behavior.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import hackerbot_helper as hhp
import time
import os

import sys
from select import select
from base_teleop import KBHit

class HeadTeleop:
    def __init__(self):
        self.kb = KBHit()

        self.robot = hhp.ProgrammedController()
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        # self.robot.leave_base()
        self.robot.get_ping() 
        
        # Modify movement parameters
        self.joint_speed = 50
        self.step_size = 0.2 # mm

        self.yaw = 180
        self.pitch = 180

        self.stop = False
        self.last_key = None  # Track last keypress
        
        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def print_terminal_instructions(self):
        """Print static instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n" + "="*10 + " Robot Head Teleop Controls " + "="*10 + "\r")
        print("   u/i : Yaw rotate L/R")
        print("   j/k : Pitch rotate B/F")
        
        print("\nOther Controls:")
        print("   p/o : increase/decrease step size")
        print("   -/+ : decrease/increase speed")
        print("\nCTRL-C or 0 to quit")
        
        # Reserve space for dynamic updates
        print("\n" + "=" * 43 + "\r")

    def update_display(self):
        """Update step size and speed in place without adding new lines"""
        sys.stdout.write(f"\rCurrent step size: {self.step_size:.1f}   |   Current speed: {self.joint_speed}%    ")
        sys.stdout.flush()  # Ensure immediate update


    def get_head_command(self):
        key = None
        # Read keyboard input
        if self.kb.kbhit() is not None:
            key = self.kb.getch()
            
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
                sys.stdin.read(1)

            if key == self.last_key:
                self.last_key = None
                return None, None  

            self.last_key = key

            # Check for quit conditions
            if key == '0':  # ESC or Ctrl-C
                self.stop = True
                return None, None
            
            if key == 'o':
                self.step_size += 0.1
            elif key == 'p':
                self.step_size -= 0.1
            if key == '-':
                self.joint_speed -= 10
                if self.joint_speed < 0:
                    self.joint_speed = 0
            elif key == '+':
                self.joint_speed += 10
                if self.joint_speed > 100:
                    self.joint_speed = 100

            return self.get_head_value_from_key(key)
        else:
            self.last_key = None
            return None, None

    def get_head_value_from_key(self, key):
        # Joint controls
        if key == 'u':    # Joint 1 left
            self.yaw += self.step_size*100
            self.yaw = max(100, min(260, self.yaw))
        elif key == 'i':  # Joint 1 right
            self.yaw -= self.step_size*100
            self.yaw = max(100, min(260, self.yaw))
        elif key == 'j':  # Joint 2 left
            self.pitch += self.step_size*100
            self.pitch = max(150, min(250, self.pitch))
        elif key == 'k':  # Joint 2 right
            self.pitch -= self.step_size*100
            self.pitch = max(150, min(250, self.pitch))
        else:
            return None, None
        
        return self.yaw, self.pitch

    def run(self):
        while not self.stop:
            y, p = self.get_head_command()
            if y is not None and p is not None:
                response = self.robot.move_head(y, p, self.joint_speed)

            time.sleep(0.2)
            if response == False:
                break
            self.update_display()

    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Restore terminal settings
            self.kb.set_normal_term()
            # Dock the robot
            # self.robot.dock()
            self.robot.move_head(180,180,50) 
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
        teleop = HeadTeleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()