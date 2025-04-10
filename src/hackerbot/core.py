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
# This module contains the Core component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time
import json

class Core():    
    def __init__(self, controller: HackerbotHelper):
        """
        Initialize Core component with HackerbotHelper object
        
        :param controller: HackerbotHelper object
        """
        self.tofs_enabled = controller._tofs_enabled
        self.json_response = controller._json_mode

        self._controller = controller

        self.ping() # Ping to check attached components

    def ping(self):
        """
        Pings the main controller to check component statuses and returns a JSON-style string
        indicating the status of the components.
        This is called during set up.

        :return: JSON-style string of component statuses or None if there is an error
        """
        try:
            self._controller.check_controller_init()
            self._controller.send_raw_command("PING")
            time.sleep(0.1)
            response = self._controller.get_json_from_command("ping")
            if response is None:
                raise Exception("No response from main controller")

            # Build JSON-style dict for robot state (excluding warnings)
            robots_state = {
                "main_controller_attached": False,
                "temperature_sensor_attached": False,
                "audio_mouth_eyes_attached": False,
                "dynamixel_controller_attached": False,
                "arm_control_attached": False
            }

            # Check component statuses
            self._controller._main_controller_attached = response.get("main_controller") == "attached"
            self._controller._temperature_sensor_attached = response.get("temperature_sensor") == "attached"
            self._controller._left_tof_attached = response.get("left_tof") == "attached"
            self._controller._right_tof_attached = response.get("right_tof") == "attached"
            self._controller._audio_mouth_eyes_attached = response.get("audio_mouth_eyes") == "attached"
            self._controller._dynamixel_controller_attached = response.get("dynamixel_controller") == "attached"
            self._controller._arm_attached = response.get("arm_controller") == "attached"

            if not self._controller._main_controller_attached:
                self._controller.log_warning("Main controller not attached")
            if not self._controller._temperature_sensor_attached:
                self._controller.log_warning("Temperature sensor not attached")
            if not self._controller._left_tof_attached:
                self._controller.log_warning("Left TOF not attached")
            if not self._controller._right_tof_attached:
                self._controller.log_warning("Right TOF not attached")

            # Update status
            robots_state["main_controller_attached"] = self._controller._main_controller_attached
            robots_state["temperature_sensor_attached"] = self._controller._temperature_sensor_attached
            robots_state["left_tof_attached"] = self._controller._left_tof_attached
            robots_state["right_tof_attached"] = self._controller._right_tof_attached
            robots_state["audio_mouth_eyes_attached"] = self._controller._audio_mouth_eyes_attached
            robots_state["dynamixel_controller_attached"] = self._controller._dynamixel_controller_attached
            robots_state["arm_control_attached"] = self._controller._arm_attached
            # Convert to JSON string (excluding warnings) before returning
            return json.dumps(robots_state, indent=2)

        except Exception as e:
            self._controller.log_error(f"Error in core:ping: {e}")
            return None

    def versions(self):
        """
        Get the version numbers of the main controller, audio mouth eyes, dynamixel controller, and arm controller.

        :return: A JSON string containing the version numbers of the components.
        """
        try:
            self._controller.check_controller_init()
            self._controller.send_raw_command("VERSION")
            time.sleep(0.1)
            response = self._controller.get_json_from_command("version")
            if response is None:
                raise Exception("No response from main controller")

            # Build response dictionary with all relevant version info
            version_info = {
                "main_controller_version": response.get("main_controller"),
                "audio_mouth_eyes_version": response.get("audio_mouth_eyes"),
                "dynamixel_controller_version": response.get("dynamixel_controller"),
                "arm_controller_version": response.get("arm_controller")
            }

            return json.dumps(version_info, indent=2)

        except Exception as e:
            self._controller.log_error(f"Error in core:versions: {e}")
            return None