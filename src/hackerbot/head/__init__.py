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
# This module contains the Head component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper
from .eyes import Eyes

class Head():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller
        self.idle_mode = True

        self.setup()
        self.eyes = Eyes(self._controller)

    def setup(self):
        if not self._controller._dynamixel_controller_attached:
            self._controller.log_warning("Dynamixel controller not attached, can't control head.")
        if not self._controller._audio_mouth_eyes_attached:
            self._controller.log_warning("Audio mouth and eyes not attached, can't control eyes.")

        self.set_idle_mode(True)
        
    def look(self, yaw, pitch, speed):
        try:
            self._controller.send_raw_command(f"H_LOOK, {yaw}, {pitch}, {speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in head:look: {e}")
            return False
        
    def set_idle_mode(self, mode):
        try:
            if mode:
                self._controller.send_raw_command("H_IDLE, 1")
            else:
                self._controller.send_raw_command("H_IDLE, 0")
            # Not fetching json response since machine mode not implemented
            self.idle_mode = mode
            return True
        except Exception as e:
            self._controller.log_error(f"Error in head:set_idle_mode: {e}")
            return False