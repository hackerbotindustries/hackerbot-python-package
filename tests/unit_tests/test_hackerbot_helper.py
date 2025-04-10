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
# This module contains the unit tests for the HackerbotHelper class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import patch, MagicMock, call
import time
import logging
from hackerbot.utils.serial_helper import SerialHelper
from hackerbot.utils.hackerbot_helper import HackerbotHelper

class TestHackerbotHelper(unittest.TestCase):

    def test_setup_success(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_board_and_port', return_value= ('mock_board', 'mock_port')), \
             patch.object(HackerbotHelper, 'set_json_mode', return_value= None):
            helper = HackerbotHelper()
            helper.setup()
            
            self.assertTrue(helper._main_controller_init)

    def test_setup_port_and_board_failure(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_board_and_port', side_effect= Exception("Setup error")), \
             patch.object(HackerbotHelper, 'set_json_mode', return_value= None):
            try:
                helper = HackerbotHelper()
                helper.setup()
                
                self.assertFalse(helper._main_controller_init)
            except Exception as e:
                self.assertIn("Error in setting up hackerbot helper", str(e))

    def test_setup_json_mode_failure(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_board_and_port', return_value= ('mock_board', 'mock_port')), \
             patch.object(HackerbotHelper, 'set_json_mode', side_effect= Exception("Setup error")):
            try:
                helper = HackerbotHelper()
                helper.setup()
                
                self.assertFalse(helper._main_controller_init)
            except Exception as e:
                self.assertIn("Error in setting up hackerbot helper", str(e))

    def test_get_current_action(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_state', return_value= "ACTION"):
            helper = HackerbotHelper()
        
            result = helper.get_current_action()
        
            self.assertEqual(result, "ACTION")

    def test_set_json_mode_success(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'send_raw_command', return_value= None), \
             patch.object(SerialHelper, 'get_json_from_command', return_value= {"command": "json", "success": "true"}):
            controller = HackerbotHelper()
            controller._json_mode = False
        
            controller.set_json_mode(True)
        
            self.assertTrue(controller._json_mode)

            controller.set_json_mode(False)
        
            self.assertFalse(controller._json_mode)

    def test_set_json_mode_failure(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'send_raw_command', return_value= None), \
             patch.object(SerialHelper, 'get_json_from_command', return_value= None):
            try:
                controller = HackerbotHelper()
                controller._json_mode = False
            
                controller.set_json_mode(True)

            except Exception as e:
                self.assertIn("Error in set_json_mode", str(e))
                self.assertFalse(controller._json_mode)

    
    def test_set_tofs_success(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'send_raw_command', return_value= None), \
             patch.object(SerialHelper, 'get_json_from_command', return_value= {"command": "tofs", "success": "true"}):
            controller = HackerbotHelper()
            controller._left_tof_attached = True
            controller._right_tof_attached = True
            controller._tofs_enabled = False
        
            controller.set_TOFs(True)
        
            self.assertTrue(controller._tofs_enabled)

            controller.set_TOFs(False)
        
            self.assertFalse(controller._tofs_enabled)

    def test_set_tofs_failure(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'send_raw_command', return_value= None), \
             patch.object(SerialHelper, 'get_json_from_command', return_value= None):
            try:
                controller = HackerbotHelper()
                controller._left_tof_attached = True
                controller._right_tof_attached = True
                controller._tofs_enabled = False
            
                controller.set_TOFs(True)

            except Exception as e:
                self.assertIn("Error in set_TOFs", str(e))
                self.assertFalse(controller._tofs_enabled)

    def test_set_tofs_not_attached_failure(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'send_raw_command', return_value= None), \
             patch.object(SerialHelper, 'get_json_from_command', return_value= {"command": "tofs", "success": "true"}):
            controller = HackerbotHelper()
            controller._tofs_enabled = False
            try:
                controller._left_tof_attached = True
                controller._right_tof_attached = False
                controller.set_TOFs(True)
            except Exception as e:
                self.assertIn("Error in set_TOFs", str(e))
                self.assertFalse(controller._tofs_enabled)
            try:
                controller._left_tof_attached = False
                controller._right_tof_attached = True
                controller.set_TOFs(True)
            except Exception as e:
                self.assertIn("Error in set_TOFs", str(e))
                self.assertFalse(controller._tofs_enabled)
            try:
                controller._left_tof_attached = False
                controller._right_tof_attached = False
                controller.set_TOFs(True)
            except Exception as e:
                self.assertIn("Error in set_TOFs", str(e))
                self.assertFalse(controller._tofs_enabled)

    def test_get_current_action(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_state', return_value= "STATE"):
            controller = HackerbotHelper()
        
            result = controller.get_current_action()
        
            self.assertEqual(result, "STATE")
            
    def test_get_error_with_ser_error(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_ser_error', return_value= "Serial error"):
            controller = HackerbotHelper()
            controller._error_msg = "Controller error"
        
            result = controller.get_error()
        
            self.assertEqual(result, "Serial error")
        
    def test_get_error_with_no_ser_error(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_ser_error', return_value= None):
            controller = HackerbotHelper()
            controller._error_msg = "Controller error"
        
            result = controller.get_error()
        
            self.assertEqual(result, "Controller error")

    def test_log_error(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None):
            controller = HackerbotHelper()
            controller._v_mode = True
        
            controller.log_error("Error message")
        
            self.assertIn("Error message", controller._error_msg)

    def test_log_warning(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None):
            controller = HackerbotHelper()
            controller._v_mode = True
        
            controller.log_warning("Warning message")
        
            self.assertIn("Warning message", controller._warning_msg)
        
    def test_destroy_success(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'disconnect_serial', return_value= None):
            controller = HackerbotHelper()
            controller._main_controller_init = True
            result = controller.destroy()
            
            self.assertTrue(result)
            self.assertFalse(controller._main_controller_init)
        
    def test_destroy_failure(self):
        with patch.object(HackerbotHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'disconnect_serial', side_effect= ConnectionError("Error closing serial connection:")):
            controller = HackerbotHelper()
            controller._main_controller_init = True
            controller._v_mode = True
            
            result = controller.destroy()
            
            self.assertFalse(result)
            self.assertIn("Error in destroy", controller._error_msg)

if __name__ == '__main__':
    unittest.main()