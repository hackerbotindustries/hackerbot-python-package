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
# This module contains the unit tests for the maps class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import patch, MagicMock
from hackerbot.base.maps import Maps

class TestHackerbotMaps(unittest.TestCase):
    def setUp(self):
        self.mock_controller = MagicMock()
        self.maps = Maps(controller=self.mock_controller)

    @patch("time.sleep", return_value=None)
    def test_fetch_success(self, _):
        self.mock_controller.get_json_from_command.return_value = {
            "compressedmapdata": "fake_map_data"
        }

        result = self.maps.fetch("map123")

        self.mock_controller.send_raw_command.assert_called_with("B_MAPDATA,map123")
        self.mock_controller.get_json_from_command.assert_called_with("mapdata")
        self.assertEqual(result, "fake_map_data")

    @patch("time.sleep", return_value=None)
    def test_fetch_no_data(self, _):
        self.mock_controller.get_json_from_command.return_value = None
        result = self.maps.fetch("map123")

        self.assertIsNone(result)
        self.mock_controller.log_error.assert_called_once()

    @patch("time.sleep", return_value=None)
    def test_list_success(self, _):
        self.mock_controller.get_json_from_command.return_value = {
            "map_ids": ["m1", "m2"]
        }

        result = self.maps.list()

        self.mock_controller.send_raw_command.assert_called_with("B_MAPLIST")
        self.assertEqual(result, ["m1", "m2"])

    @patch("time.sleep", return_value=None)
    def test_list_failure(self, _):
        self.mock_controller.get_json_from_command.return_value = None

        result = self.maps.list()

        self.assertIsNone(result)
        self.mock_controller.log_error.assert_called_once()

    @patch("time.sleep", return_value=None)
    def test_position_success(self, _):
        self.mock_controller.get_json_from_command.return_value = {
            "map_id": "map01",
            "pose_x": 1.1,
            "pose_y": 2.2,
            "pose_angle": 45.5
        }

        result = self.maps.position()

        self.mock_controller.send_raw_command.assert_called_with("B_POSE")
        self.assertEqual(result, {"x": 1.1, "y": 2.2, "angle": 45.5})
        self.assertEqual(self.maps.map_id, "map01")
        self.assertEqual(self.maps._x, 1.1)
        self.assertEqual(self.maps._y, 2.2)
        self.assertEqual(self.maps._angle, 45.5)

    @patch("time.sleep", return_value=None)
    def test_position_failure(self, _):
        self.mock_controller.get_json_from_command.return_value = None

        result = self.maps.position()

        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_once()

    @patch("time.sleep", return_value=None)
    def test_goto_success_docked(self, _):
        self.maps._docked = True
        self.maps._goto_completed = False

        self.maps._x = 1.0
        self.maps._y = 2.0
        self.maps._angle = 90
        self.maps._goal_x = 1.0
        self.maps._goal_y = 2.0
        self.maps._goal_angle = 90

        self.maps.position = MagicMock(return_value={"x": 1.0, "y": 2.0, "angle": 90})
        self.maps._calculate_position_offset = MagicMock(side_effect=self._complete_goto)

        result = self.maps.goto(1.0, 2.0, 90, 0.3)

        self.assertTrue(result)
        self.assertFalse(self.maps._docked)
        self.mock_controller.send_raw_command.assert_called_with("B_GOTO,1.0,2.0,90,0.3")

    def _complete_goto(self):
        self.maps._goto_completed = True

    @patch("time.sleep", return_value=None)
    def test_goto_failure(self, _):
        self.mock_controller.send_raw_command.side_effect = Exception("Command failed")

        result = self.maps.goto(0, 0, 0, 0.5)

        self.assertFalse(result)
        self.mock_controller.log_error.assert_called_once()

    def test_calculate_position_offset_completes(self):
        self.maps._x = 5.0
        self.maps._y = 5.0
        self.maps._angle = 180
        self.maps._goal_x = 5.05
        self.maps._goal_y = 5.05
        self.maps._goal_angle = 180

        self.maps._calculate_position_offset()

        self.assertTrue(self.maps._goto_completed)

    def test_calculate_position_offset_incomplete(self):
        self.maps._x = 1.0
        self.maps._y = 1.0
        self.maps._angle = 0
        self.maps._goal_x = 10.0
        self.maps._goal_y = 10.0
        self.maps._goal_angle = 180

        self.maps._calculate_position_offset()

        self.assertFalse(self.maps._goto_completed)

    @patch("time.sleep", return_value=None)
    def test_wait_until_reach_pose_works(self, _):
        self.maps.position = MagicMock()
        self.maps._calculate_position_offset = MagicMock(side_effect=self._complete_goto)
        self.maps._goto_completed = False

        self.maps._wait_until_reach_pose()

        self.maps.position.assert_called()
        self.maps._calculate_position_offset.assert_called()
        self.assertFalse(self.maps._goto_completed)  # should reset after reaching


if __name__ == "__main__":
    unittest.main()