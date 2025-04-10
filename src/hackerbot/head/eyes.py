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
# This module contains the Eyes component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper

class Eyes():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller

    def gaze(self, x, y):
        """
        Move the eyes to the specified position in the view.

        Args:
        x (float): x position between -1.0 and 1.0
        y (float): y position between -1.0 and 1.0

        Returns:
        bool: Whether the command was successful
        """
        try:
            self._controller.send_raw_command(f"H_GAZE,{x},{y}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in eyes:gaze: {e}")
            return False