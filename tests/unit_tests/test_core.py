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
# This module contains the unit tests for the core class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################

import json
import unittest
from unittest.mock import patch, MagicMock, call
import time
import logging
from hackerbot.utils.hackerbot_helper import HackerbotHelper
from hackerbot.core import Core

class TestHackerbotCore(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock()

        # Mock attributes
        self.mock_controller._tofs_enabled = True
        self.mock_controller._json_mode = True

        # Mock method behaviors
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None
            
    def test_ping_success(self):
        sample_response = {
            "main_controller": "attached",
            "temperature_sensor": "attached",
            "left_tof": "attached",
            "right_tof": "attached",
            "audio_mouth_eyes": "attached",
            "dynamixel_controller": "attached",
            "arm_controller": "attached"
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None


        core = Core(self.mock_controller)

        expected_output = {
            "main_controller_attached": True,
            "temperature_sensor_attached": True,
            "left_tof_attached": True,
            "right_tof_attached": True,
            "audio_mouth_eyes_attached": True,
            "dynamixel_controller_attached": True,
            "arm_control_attached": True,
        }

        result = core.ping()
        self.assertEqual(json.loads(result), expected_output)
        self.assertTrue(self.mock_controller._main_controller_attached)
        self.assertTrue(self.mock_controller._temperature_sensor_attached)
        self.assertTrue(self.mock_controller._left_tof_attached)
        self.assertTrue(self.mock_controller._right_tof_attached)
        self.assertTrue(self.mock_controller._audio_mouth_eyes_attached)
        self.assertTrue(self.mock_controller._dynamixel_controller_attached)
        self.assertTrue(self.mock_controller._arm_attached)

    def test_ping_main_controller_not_attached(self):
        sample_response = {
            # "main_controller": "attached", # Main controller not attached
            "temperature_sensor": "attached",
            "left_tof": "attached",
            "right_tof": "attached",
            "audio_mouth_eyes": "attached",
            "dynamixel_controller": "attached",
            "arm_controller": "attached"
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None


        core = Core(self.mock_controller)

        expected_output = {
            "main_controller_attached": False,
            "temperature_sensor_attached": True,
            "left_tof_attached": True,
            "right_tof_attached": True,
            "audio_mouth_eyes_attached": True,
            "dynamixel_controller_attached": True,
            "arm_control_attached": True,
        }

        result = core.ping()
        self.assertEqual(json.loads(result), expected_output)
        self.assertFalse(self.mock_controller._main_controller_attached)
        self.assertTrue(self.mock_controller._temperature_sensor_attached)
        self.assertTrue(self.mock_controller._left_tof_attached)
        self.assertTrue(self.mock_controller._right_tof_attached)
        self.assertTrue(self.mock_controller._audio_mouth_eyes_attached)
        self.assertTrue(self.mock_controller._dynamixel_controller_attached)
        self.assertTrue(self.mock_controller._arm_attached)
        self.mock_controller.log_warning.assert_called_with("Main controller not attached")
        
    def test_ping_temperature_sensor_not_attached(self):
        sample_response = {
            "main_controller": "attached", 
            # "temperature_sensor": "attached", # Temperature sensor not attached
            "left_tof": "attached",
            "right_tof": "attached",
            "audio_mouth_eyes": "attached",
            "dynamixel_controller": "attached",
            "arm_controller": "attached"
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None


        core = Core(self.mock_controller)

        expected_output = {
            "main_controller_attached": True,
            "temperature_sensor_attached": False,
            "left_tof_attached": True,
            "right_tof_attached": True,
            "audio_mouth_eyes_attached": True,
            "dynamixel_controller_attached": True,
            "arm_control_attached": True,
        }

        result = core.ping()
        self.assertEqual(json.loads(result), expected_output)
        self.assertTrue(self.mock_controller._main_controller_attached)
        self.assertFalse(self.mock_controller._temperature_sensor_attached)
        self.assertTrue(self.mock_controller._left_tof_attached)
        self.assertTrue(self.mock_controller._right_tof_attached)
        self.assertTrue(self.mock_controller._audio_mouth_eyes_attached)
        self.assertTrue(self.mock_controller._dynamixel_controller_attached)
        self.assertTrue(self.mock_controller._arm_attached)
        self.mock_controller.log_warning.assert_called_with("Temperature sensor not attached")

    def test_ping_tofs_not_attached(self):
        sample_response = {
            "main_controller": "attached", 
            "temperature_sensor": "attached", 
            # "left_tof": "attached", # Left TOF not attached
            # "right_tof": "attached", # Right TOF not attached
            "audio_mouth_eyes": "attached",
            "dynamixel_controller": "attached",
            "arm_controller": "attached"
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None


        core = Core(self.mock_controller)

        expected_output = {
            "main_controller_attached": True,
            "temperature_sensor_attached": True,
            "left_tof_attached": False,
            "right_tof_attached": False,
            "audio_mouth_eyes_attached": True,
            "dynamixel_controller_attached": True,
            "arm_control_attached": True,
        }

        result = core.ping()
        self.assertEqual(json.loads(result), expected_output)
        self.assertTrue(self.mock_controller._main_controller_attached)
        self.assertTrue(self.mock_controller._temperature_sensor_attached)
        self.assertFalse(self.mock_controller._left_tof_attached)
        self.assertFalse(self.mock_controller._right_tof_attached)
        self.assertTrue(self.mock_controller._audio_mouth_eyes_attached)
        self.assertTrue(self.mock_controller._dynamixel_controller_attached)
        self.assertTrue(self.mock_controller._arm_attached)
        # self.mock_controller.log_warning.assert_called_with("Left TOF not attached")
        self.mock_controller.log_warning.assert_called_with("Right TOF not attached")

    def test_ping_head_arm_not_attached(self):
        sample_response = {
            "main_controller": "attached", 
            "temperature_sensor": "attached", 
            "left_tof": "attached",
            "right_tof": "attached",
            # "audio_mouth_eyes": "attached", 
            # "dynamixel_controller": "attached",
            # "arm_controller": "attached"
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None


        core = Core(self.mock_controller)

        expected_output = {
            "main_controller_attached": True,
            "temperature_sensor_attached": True,
            "left_tof_attached": True,
            "right_tof_attached": True,
            "audio_mouth_eyes_attached": False,
            "dynamixel_controller_attached": False,
            "arm_control_attached": False,
        }

        result = core.ping()
        self.assertEqual(json.loads(result), expected_output)
        self.assertTrue(self.mock_controller._main_controller_attached)
        self.assertTrue(self.mock_controller._temperature_sensor_attached)
        self.assertTrue(self.mock_controller._left_tof_attached)
        self.assertTrue(self.mock_controller._right_tof_attached)
        self.assertFalse(self.mock_controller._audio_mouth_eyes_attached)
        self.assertFalse(self.mock_controller._dynamixel_controller_attached)
        self.assertFalse(self.mock_controller._arm_attached)

    def test_versions_success(self):
        sample_response = {
            "main_controller": "v7", 
            "audio_mouth_eyes": "v7", 
            "dynamixel_controller": "v7",
            "arm_controller": "v7"
        }

        self.mock_controller.get_json_from_command.return_value = sample_response
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None


        core = Core(self.mock_controller)

        expected_output = {
            "main_controller_version": "v7",
            "audio_mouth_eyes_version": "v7",
            "dynamixel_controller_version": "v7",
            "arm_controller_version": "v7"
        }

        result = core.versions()
        self.assertEqual(json.loads(result), expected_output)
        
    def test_versions_failure(self):
        self.mock_controller.get_json_from_command.return_value = None
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None

        core = Core(self.mock_controller)

        result = core.versions()
        self.assertEqual(result, None)
        self.mock_controller.log_error.assert_called_with("Error in core:versions: No response from main controller")