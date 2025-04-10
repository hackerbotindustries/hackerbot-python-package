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
# This module contains the unit tests for the Base class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################

import json
import unittest
from unittest.mock import patch, MagicMock, call
from hackerbot.utils.hackerbot_helper import HackerbotHelper
from hackerbot.base import Base

class TestHackerbotBase(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock()
        # Mock method behaviors
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

    def test_initialize_success(self):
        # self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None
        self.mock_controller._base_init = False

        base = Base(self.mock_controller)
 
        result = base.initialize()
        
        self.assertTrue(result)
        self.assertTrue(self.mock_controller._base_init)

    def test_set_mode_success(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)

        result = base.set_mode(0)
        
        self.assertTrue(result)

    def test_status_success(self):
        sample_response = {
            "timestamp": "2023-06-01T00:00:00.000Z",
            "left_encoder": 0,
            "right_encoder": 0,
            "left_speed": 0,
            "right_speed": 0,
            "left_set_speed": 0,
            "right_set_speed": 0,
            "wall_tof": 0,
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)
        base._future_completed = False

        result = base.status()
        self.assertEqual(result, sample_response)
        self.assertTrue(base._future_completed)

        new_response = {
            "timestamp": "2023-06-01T00:00:00.000Z",
            "left_encoder": 0,
            "right_encoder": 0,
            "left_speed": 0,
            "right_speed": 0,
            "left_set_speed": 10,
            "right_set_speed": 0,
            "wall_tof": 0,
        }

        self.mock_controller.get_json_from_command.return_value = new_response
        result = base.status()
        self.assertEqual(result, new_response)
        self.assertFalse(base._future_completed)

    def test_status_failure(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)

        result = base.status()
        self.assertEqual(result, None)
        self.mock_controller.log_error.assert_called_with("Error in base:status: Status command failed")
        
        
    def test_start_success(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)
        base._future_completed = True
        base._docked = True

        result = base.start()
        self.assertFalse(base._docked)
        self.assertFalse(base._future_completed)
        self.assertTrue(result)
        
    def test_quickmap_success(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)
        base._future_completed = True

        result = base.quickmap()
        self.assertFalse(base._future_completed)
        self.assertTrue(result)
        
    def test_dock_success(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)
        base._future_completed = True
        base._docked = False

        result = base.dock()

        self.assertFalse(base._future_completed)
        self.assertTrue(base._docked)
        self.assertTrue(result)
    
    def test_kill_success(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None
        self.mock_controller._base_init = True

        base = Base(self.mock_controller)

        result = base.kill()

        self.assertFalse(self.mock_controller._base_init)
        self.assertTrue(result)
        
    def test_trigger_bump_success(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        base = Base(self.mock_controller)

        result = base.trigger_bump(True, True)

        self.assertTrue(result)

    def test_drive_success(self):
        self.mock_controller.get_json_from_command.return_value = {"command": "drive", "success": "true"}
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None
        self.mock_controller._driver_mode = True

        base = Base(self.mock_controller)
        base._future_completed = True

        result = base.drive(0, 0)

        self.assertFalse(base._future_completed)
        self.assertTrue(result)

    def test_drive_failure(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None
        self.mock_controller._driver_mode = True

        base = Base(self.mock_controller)
        base._future_completed = True

        result = base.drive(0, 0)

        self.assertTrue(base._future_completed)
        self.assertFalse(result)    