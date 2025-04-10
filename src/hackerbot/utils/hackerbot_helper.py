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
# This module contains the HackerbotHelper class, which is a subclass of SerialHelper.
# It contains the fields that will be share among higher level classes.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from .serial_helper import SerialHelper
import time
import logging

class HackerbotHelper(SerialHelper):
    def __init__(self, port=None, board=None, verbose_mode=False):
        self._error_msg = ""
        self._warning_msg = ""
        self._v_mode = verbose_mode
        self._main_controller_init = False  # Ensure this is set before exception handling

        self._json_mode = False

        self._main_controller_attached = False
        self._temperature_sensor_attached = False

        self._left_tof_attached = False
        self._right_tof_attached = False

        self._tofs_enabled = False
        
        self._base_init = False
        self._driver_mode = False
        
        self._audio_mouth_eyes_attached = False
        self._dynamixel_controller_attached = False

        self._arm_attached = False
        
        self._port = port
        self._board = board

        self.setup()


    def setup(self):
        """
        Initialize the main controller.

        If self._port and self._board are None, this method will find the first available serial port and use it to initialize the main controller.
        Otherwise, it will use the provided port and board to initialize.
        After initialization, it will set the main controller to JSON mode and enable the TOFs.
        This setup ensures json mode are set and controller is initialized properly.
        If an exception occurs during initialization, it will raise an exception with the error message.
        """
        try:
            if self._port is None or self._board is None:
                super().__init__()
                self._board, self._port = super().get_board_and_port()
            else:
                super().__init__(self._port, self._board)

            self._main_controller_init = True
            self.set_json_mode(True)
            # self.set_TOFs(True)
        except Exception as e:
            raise Exception(f"Error in setting up hackerbot helper: {e}")

    # Activate JSON mode
    def set_json_mode(self, mode):
        try:
            if mode == True:
                super().send_raw_command("JSON, 1")
                time.sleep(0.1) # Short sleep to process json response
                response = super().get_json_from_command("json")
                if response is None:
                    raise Exception("Failed to set json mode to: ", mode)
            else:
                super().send_raw_command("JSON, 0")
            self._json_mode = mode
        except Exception as e:
            raise Exception(f"Error in set_json_mode: {e}")

    #Set TOFs
    def set_TOFs(self, mode):
        try:
            if not self._left_tof_attached or not self._right_tof_attached:
                raise Exception("TOFs not attached")
            if mode == True:
                super().send_raw_command("TOFS, 1")
            else:
                super().send_raw_command("TOFS, 0")
            time.sleep(0.1) # Short sleep to process json response
            response = super().get_json_from_command("tofs")
            if response is None:
                raise Exception("TOFs activation failed")
            self._tofs_enabled = mode
        except Exception as e:
            raise Exception(f"Error in set_TOFs: {e}")

    def get_current_action(self):
        return super().get_state()
    
    def get_error(self):
        # Serial error should be priority
        if super().get_ser_error() is not None:
            return super().get_ser_error()
        else:
            return self._error_msg

    def log_error(self, error):
        if self._v_mode:
            logging.error(error)
        self._error_msg = error

    def log_warning(self, warning):
        if self._v_mode:
            logging.warning(warning)
        self._warning_msg = warning

    def check_controller_init(self):
        if not self._main_controller_init:
            raise Exception("Main controller not initialized.")
        if not self._json_mode:
            raise Exception("JSON mode not enabled.")

    def destroy(self):
        try:
            super().disconnect_serial()
            self._main_controller_init = False
            return True
        except Exception as e:
            self.log_error(f"Error in destroy: {e}")
            return False