################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.10
#
# This module contains the unit tests for the head class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import patch, MagicMock
from hackerbot.head import Head
from hackerbot.head.eyes import Eyes 

class TestHackerbotHead(unittest.TestCase):
    def setUp(self):
        self.mock_controller = MagicMock()
        self.mock_controller._dynamixel_controller_attached = True
        self.mock_controller._audio_mouth_eyes_attached = True
        self.head = Head(controller=self.mock_controller)

    def test_setup_all_attached(self):
        self.mock_controller.reset_mock()
        self.head.setup()
        self.mock_controller.log_warning.assert_not_called()
        self.mock_controller.send_raw_command.assert_called_with("H_IDLE, 1")

    def test_setup_missing_dynamixel(self):
        self.mock_controller._dynamixel_controller_attached = False
        self.mock_controller._audio_mouth_eyes_attached = True
        head = Head(controller=self.mock_controller)
        self.mock_controller.log_warning.assert_called_with("Dynamixel controller not attached, can't control head.")

    def test_setup_missing_eyes_audio(self):
        self.mock_controller._dynamixel_controller_attached = True
        self.mock_controller._audio_mouth_eyes_attached = False
        head = Head(controller=self.mock_controller)
        self.mock_controller.log_warning.assert_called_with("Audio mouth and eyes not attached, can't control eyes.")

    def test_eyes_initialized(self):
        self.assertIsNotNone(self.head.eyes)
        self.assertEqual(self.head.eyes._controller, self.mock_controller)

    def test_look_success(self):
        result = self.head.look(30, 15, 80)
        self.assertTrue(result)
        self.mock_controller.send_raw_command.assert_called_with("H_LOOK, 30, 15, 80")

    def test_look_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("look fail")
        result = self.head.look(10, 5, 50)
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_with("Error in head:look: look fail")

    def test_set_idle_mode_true(self):
        result = self.head.set_idle_mode(True)
        self.assertTrue(result)
        self.assertTrue(self.head.idle_mode)
        self.mock_controller.send_raw_command.assert_called_with("H_IDLE, 1")

    def test_set_idle_mode_false(self):
        result = self.head.set_idle_mode(False)
        self.assertTrue(result)
        self.assertFalse(self.head.idle_mode)
        self.mock_controller.send_raw_command.assert_called_with("H_IDLE, 0")

    def test_set_idle_mode_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("idle mode fail")
        result = self.head.set_idle_mode(True)
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_with("Error in head:set_idle_mode: idle mode fail")

class TestEyes(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock()
        self.eyes = Eyes(controller=self.mock_controller)

    def test_gaze_success(self):
        self.eyes._controller.send_raw_command = MagicMock()
        result = self.eyes.gaze(0.5, -0.5)
        self.assertTrue(result)
        self.eyes._controller.send_raw_command.assert_called_with("H_GAZE,0.5,-0.5")

    def test_gaze_failure(self):
        self.eyes._controller.send_raw_command.side_effect = Exception("gaze error")
        self.eyes._controller.log_error = MagicMock()
        result = self.eyes.gaze(-1.0, 1.0)
        self.assertFalse(result)
        self.eyes._controller.log_error.assert_called_with("Error in eyes:gaze: gaze error")

if __name__ == '__main__':
    unittest.main()
