################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.07
#
# This module contains the Arm component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper
from .gripper import Gripper

class Arm():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller
        self.idle_mode = True

        self.setup()
        self.gripper = Gripper(self._controller)

    def setup(self):
       if not self._controller._arm_attached:
            self._controller.log_warning("Arm not attached, can't control arm.")

    def move_joint(self, joint_id, angle, speed):
        """
        Moves a single joint of the robotic arm to a specified angle at a given speed.

        Args:
            joint_id (int): Joint number from 1 to 6. Joint 1 is the base and is in order moving up the arm.
            angle (float): Angle for the specified joint. Valid range is -165.0 to 165.0 degrees for joints 1 to 5 and -175.0 to 175.0 for joint 6.
            speed (int): Speed at which the arm moves to the new position. Valid range is 0 to 100.

        Returns:
            bool: True if the movement command was successfully sent, False if an error occurred.
        """
        try:
            self._controller.send_raw_command(f"A_ANGLE,{joint_id},{angle},{speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in arm:move_joint: {e}")
            return False
    
    def move_joints(self, j_agl_1, j_agl_2, j_agl_3, j_agl_4, j_agl_5, j_agl_6, speed):
        """
        Moves all six joints of the robotic arm to specified angles at a given speed.

        Args:
            j_agl_1 (float): Angle for joint 1, base joint. Valid range is -165.0 to 165.0 degrees.
            j_agl_2 (float): Angle for joint 2. Valid range is -165.0 to 165.0 degrees.
            j_agl_3 (float): Angle for joint 3. Valid range is -165.0 to 165.0 degrees.
            j_agl_4 (float): Angle for joint 4. Valid range is -165.0 to 165.0 degrees.
            j_agl_5 (float): Angle for joint 5. Valid range is -165.0 to 165.0 degrees.
            j_agl_6 (float): Angle for joint 6. Valid range is -175.0 to 175.0 degrees.
            speed (int): Speed at which the arm moves to the new positions. Valid range is 0 to 100.

        Returns:
            bool: True if the movement command was successfully sent, False if an error occurred.
        """
        try:
            self._controller.send_raw_command(f"A_ANGLES,{j_agl_1},{j_agl_2},{j_agl_3},{j_agl_4},{j_agl_5},{j_agl_6},{speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in arm:move_joints: {e}")
            return False    
            
            