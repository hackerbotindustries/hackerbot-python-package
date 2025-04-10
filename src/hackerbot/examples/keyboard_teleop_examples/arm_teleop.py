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
# This script is an example of how to use the arm teleop behavior.
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

class ArmTeleop:
    def __init__(self):
        self.kb = KBHit()

        self.robot = hhp.ProgrammedController()
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        # self.robot.leave_base()
        self.robot.get_ping() 
        
        # Modify movement parameters
        self.arm_speed = 50
        self.step_size = 0.2 # mm

        self.j_agl_1 = 0
        self.j_agl_2 = 0
        self.j_agl_3 = 0
        self.j_agl_4 = 0
        self.j_agl_5 = 0
        self.j_agl_6 = 0

        self.stop = False
        self.last_key = None  # Track last keypress
        
        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def print_terminal_instructions(self):
        """Print static instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n" + "="*10 + " Robot Arm Teleop Controls " + "="*10 + "\r")
        
        print("\nJoint Controls (±165° for joints 1-5, ±175° for joint 6):")
        print("   q/w : Joint 1 L/R")
        print("   a/s : Joint 2 BCK/FWD")
        print("   z/x : Joint 3 BCK/FWD")
        print("   e/r : Joint 4 BCK/FWD")
        print("   d/f : Joint 5 L/R")
        print("   c/v : Joint 6 L/R")
        
        print("\nGripper Controls:")
        print("   g/h    : Open/Close gripper")
        print("   b    : Calibrate gripper")
        
        print("\nOther Controls:")
        print("   o/p : increase/decrease step size")
        print("   -/+ : decrease/increase speed")
        print("\nCTRL-C or 0 to quit")
        
        # Reserve space for dynamic updates
        print("\n" + "=" * 43 + "\r")

    def update_display(self):
        """Update step size and speed in place without adding new lines"""
        sys.stdout.write(f"\rCurrent step size: {self.step_size:.1f}   |   Current speed: {self.arm_speed}%    ")
        sys.stdout.flush()  # Ensure immediate update


    def get_arm_command(self):
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
                self.arm_speed -= 10
                if self.arm_speed < 0:
                    self.arm_speed = 0
            elif key == '+':
                self.arm_speed += 10
                if self.arm_speed > 100:
                    self.arm_speed = 100

            command, value = self.get_arm_value_from_key(key)
            return command, value
        else:
            self.last_key = None
            return None, None

    def get_arm_value_from_key(self, key):
                # Joint controls
        if key == 'q':    # Joint 1 left
            self.j_agl_1 += self.step_size*100
            return 1, self.j_agl_1
        elif key == 'w':  # Joint 1 right
            self.j_agl_1 -= self.step_size*100
            return 1, self.j_agl_1
        elif key == 'a':  # Joint 2 left
            self.j_agl_2 += self.step_size*100
            return 2, self.j_agl_2
        elif key == 's':  # Joint 2 right
            self.j_agl_2 -= self.step_size*100
            return 2, self.j_agl_2
        elif key == 'z':  # Joint 3 left
            self.j_agl_3 += self.step_size*100
            return 3, self.j_agl_3
        elif key == 'x':  # Joint 3 right
            self.j_agl_3 -= self.step_size*100
            return 3, self.j_agl_3
        elif key == 'e':  # Joint 4 left
            self.j_agl_4 += self.step_size*100
            return 4, self.j_agl_4
        elif key == 'r':  # Joint 4 right
            self.j_agl_4 -= self.step_size*100
            return 4, self.j_agl_4
        elif key == 'd':  # Joint 5 left
            self.j_agl_5 += self.step_size*100
            return 5, self.j_agl_5
        elif key == 'f':  # Joint 5 right
            self.j_agl_5 -= self.step_size*100
            return 5, self.j_agl_5
        elif key == 'c':  # Joint 6 left
            self.j_agl_6 += self.step_size*100
            return 6, self.j_agl_6
        elif key == 'v':  # Joint 6 right
            self.j_agl_6 -= self.step_size*100
            return 6, self.j_agl_6
        # Gripper controls
        elif key == 'g':  # Open gripper
            return 'gripper_open', 'True'
        elif key == 'h':  # Close gripper
            return 'gripper_close', 'True'
        elif key == 'b':  # Calibrate gripper
            return 'gripper_calibrate', 'True'
        else:
            return None, None
        

    def run(self):
        while not self.stop:
            response = None
            command, value = self.get_arm_command()
            if command is not None:
                if isinstance(command, int):  # Joint movement
                    # Limit joint angles based on which joint
                    max_angle = 175.0 if command == 6 else 165.0
                    if abs(value) <= max_angle:
                        response = self.robot.move_single_joint(command, value, self.arm_speed)

                elif command == 'gripper_open':
                    response = self.robot.open_gripper()
                elif command == 'gripper_close':
                    response = self.robot.close_gripper()
                elif command == 'gripper_calibrate':
                    response = self.robot.arm_calibrate()
                
                if response == False:
                    break
            time.sleep(0.2)
            self.update_display()

    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Restore terminal settings
            self.kb.set_normal_term()
            # Dock the robot
            # self.robot.dock()
            self.robot.move_all_joint(0,0,0,0,0,0,50) 
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
        teleop = ArmTeleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()