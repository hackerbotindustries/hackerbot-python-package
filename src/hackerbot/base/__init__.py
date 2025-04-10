################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.08
#
# This module contains the Base component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper
from .maps import Maps
import time

class Base():    
    def __init__(self, controller: HackerbotHelper):
        """
        Initialize Core component with HackerbotHelper object
        
        :param controller: HackerbotHelper object
        """
        self._controller = controller
        self.initialize() # Call before any action is done on the base

        self.maps = Maps(controller)

        self._future_completed = False
        self._docked = True # Default to true, assume always start from charger

      
    def initialize(self):
        try:
            self._controller.send_raw_command("B_INIT")
            self._controller._base_init = True
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:initialize: {e}")
            raise Exception(f"Error in initialize: {e}")
        
    def set_mode(self, mode):
        try:
            self._controller.send_raw_command(f"B_MODE,{mode}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:set_mode: {e}")
            return False
        
    def status(self):
        try:
            self._controller.send_raw_command("B_STATUS")
            time.sleep(0.1)
            response = self._controller.get_json_from_command("status")
            if response is None:
                raise Exception("Status command failed")
            
            if response.get("left_set_speed") == 0 and response.get("right_set_speed") == 0:
                self._future_completed = True
            else:
                self._future_completed = False

                        # Parse and return relevant fields
            parsed_data = {
                "timestamp": response.get("timestamp"),
                "left_encoder": response.get("left_encoder"),
                "right_encoder": response.get("right_encoder"),
                "left_speed": response.get("left_speed"),
                "right_speed": response.get("right_speed"),
                "left_set_speed": response.get("left_set_speed"),
                "right_set_speed": response.get("right_set_speed"),
                "wall_tof": response.get("wall_tof"),
            }
            return parsed_data
        except Exception as e:
            self._controller.log_error(f"Error in base:status: {e}")
            return None
        
    def start(self):
        try:
            self._controller.send_raw_command("B_START")
            # Not fetching json response since machine mode not implemented
            self._controller._driver_mode = True
            if self._docked:
                time.sleep(3)
                self._docked = False
            self._wait_until_completed()

            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:start: {e}")
            return False
        
    def quickmap(self):
        """
        Start the quick mapping process.

        This function sends a command to the base to initiate the quick mapping process.
        It first checks the system status to ensure all components are ready. If
        the quick mapping command is successfully sent, the function returns True.
        In case of any errors, it logs the error message and returns False.

        :return: True if the quick mapping command is successful, False otherwise.
        """
        try:
            self._controller.send_raw_command("B_QUICKMAP")
            # Not fetching json response since machine mode not implemented
            self._wait_until_completed()
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:quickmap: {e}")
            return False
        
    def dock(self):
        """
        Dock the base to the docking station.

        This function sends a command to the base to initiate the docking process.
        It first checks the system status to ensure all components are ready. If
        the docking command is successfully sent, the function returns True.
        In case of any errors, it logs the error message and returns False.

        :return: True if the docking command is successful, False otherwise.
        """
        try:
            self._controller.send_raw_command("B_DOCK")
            time.sleep(2)
            # Not fetching json response since machine mode not implemented
            self._wait_until_completed()
            self._docked = True
            self._controller._driver_mode = False
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:dock: {e}")
            return False


    def kill(self):
        """
        Kill the base's movement. This is a blocking call and will not return until the base is stopped.
        After calling this method, the base will not be able to move until start() is called again.
        :return: True if successful, False otherwise.
        """
        try:
            self._controller.send_raw_command("B_KILL")
            self._controller._base_init = False
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:kill: {e}")
            return False
        
    def trigger_bump(self, left, right):
        """
        Trigger the bump sensors on the base.

        :param left: 0 or 1 to disable or enable the left bump sensor.
        :param right: 0 or 1 to disable or enable the right bump sensor.
        :return: True if the command is successful, False if it fails.
        """
        left = 1 if True else 0
        right = 1 if True else 0
        try:
            self._controller.send_raw_command("B_BUMP, {0}, {1}".format(left, right))
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:trigger_bump: {e}")
            return False
        
    def drive(self, l_vel, a_vel):
        """
        Set the base velocity.

        :param l_vel: Linear velocity in mm/s. Positive is forward, negative is backward.
        :param a_vel: Angular velocity in degrees/s. Positive is counterclockwise, negative is clockwise.
        :return: True if the command is successful, False if it fails.
        """
        try:
            if not self._controller._driver_mode:
                self.start()
            self._controller.send_raw_command(f"B_DRIVE,{l_vel},{a_vel}")
            time.sleep(0.1)
            response = self._controller.get_json_from_command("drive")
            if response is None:
                raise Exception("Drive command failed")
            self._wait_until_completed()
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:drive: {e}")
            return False
        
    def _wait_until_completed(self):
        while not self._future_completed:
            self.status()
            # print(self.status())
        self._future_completed = False
        
    def destroy(self, auto_dock=False):
        """
        Clean up and shut down the base.

        This method kills the base's movement and optionally docks it before 
        destroying the controller. If `auto_dock` is set to True, the base will 
        dock before the destruction process.

        :param auto_dock: If True, the base will dock before being destroyed. Defaults to False.
        """
        self.kill()
        if auto_dock:
            time.sleep(3.0)
            self.dock()
        self._controller.destroy()