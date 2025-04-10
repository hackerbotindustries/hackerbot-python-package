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
# This module contains the unit tests for the Arm class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import patch, MagicMock
from hackerbot.arm import Arm
from hackerbot.arm.gripper import Gripper

class TestHackerbotArm(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock()
        self.mock_controller._arm_attached = True
        self.arm = Arm(controller=self.mock_controller)

    def test_setup_arm_attached(self):
        # Controller has _arm_attached True by default in setUp
        self.arm.setup()
        self.mock_controller.log_warning.assert_not_called()

    def test_setup_arm_not_attached(self):
        self.mock_controller._arm_attached = False
        self.arm.setup()
        self.mock_controller.log_warning.assert_called_once_with("Arm not attached, can't control arm.")

    def test_gripper_initialized(self):
        self.assertIsNotNone(self.arm.gripper)
        self.assertEqual(self.arm.gripper._controller, self.mock_controller)

    def test_move_joint_success(self):
        result = self.arm.move_joint(3, 90.0, 50)
        self.assertTrue(result)
        self.mock_controller.send_raw_command.assert_called_with("A_ANGLE,3,90.0,50")

    def test_move_joint_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("Fail to send command")
        result = self.arm.move_joint(2, -90.0, 50)
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_once_with("Error in arm:move_joint: Fail to send command")

    def test_move_joints_success(self):
        result = self.arm.move_joints(0, 15, -30, 45, 60, 90, 70)
        self.assertTrue(result)
        self.mock_controller.send_raw_command.assert_called_with("A_ANGLES,0,15,-30,45,60,90,70")

    def test_move_joints_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("Move joints failed")
        result = self.arm.move_joints(0, 0, 0, 0, 0, 0, 0)
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_once_with("Error in arm:move_joints: Move joints failed")



class TestGripper(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock()
        self.gripper = Gripper(controller=self.mock_controller)

    def test_calibrate_success(self):
        result = self.gripper.calibrate()
        self.assertTrue(result)
        self.mock_controller.send_raw_command.assert_called_with("A_CAL")

    def test_calibrate_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("Calibration failed")
        result = self.gripper.calibrate()
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_with("Error in gripper:calibrate: Calibration failed")

    def test_open_success(self):
        result = self.gripper.open()
        self.assertTrue(result)
        self.mock_controller.send_raw_command.assert_called_with("A_OPEN")

    def test_open_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("Open failed")
        result = self.gripper.open()
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_with("Error in gripper:open: Open failed")

    def test_close_success(self):
        result = self.gripper.close()
        self.assertTrue(result)
        self.mock_controller.send_raw_command.assert_called_with("A_CLOSE")

    def test_close_failure(self):
        self.mock_controller.send_raw_command.side_effect = Exception("Close failed")
        result = self.gripper.close()
        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_with("Error in gripper:close: Close failed")

if __name__ == '__main__':
    unittest.main()