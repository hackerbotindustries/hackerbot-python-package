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
# This module contains the Gripper component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper

class Gripper(HackerbotHelper):
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller

    def calibrate(self):
        """
        Calibrates the gripper by sending a raw calibration command.

        Returns:
            bool: True if the calibration command was successfully sent, False if an error occurred.
        """
        try:
            self._controller.send_raw_command("A_CAL")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in gripper:calibrate: {e}")
            return False
        
    def open(self):
        try:
            self._controller.send_raw_command("A_OPEN")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in gripper:open: {e}")
            return False
            
    def close(self):
        try:
            self._controller.send_raw_command("A_CLOSE")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in gripper:close: {e}")
            return False