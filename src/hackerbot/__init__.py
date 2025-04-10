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
# This is the file for the hackerbot package. It imports
# and initialized the sub components
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from .core import Core
from .base import Base
from .head import Head
from .arm import Arm
from .utils.hackerbot_helper import HackerbotHelper

class Hackerbot(HackerbotHelper):
    def __init__(self, port=None, board=None, model=None,verbose_mode=False):
        super().__init__(port, board, verbose_mode)
        # Share self (which is a HackerbotHelper) with subsystems
        self.core = Core(controller=self)
        self.base = Base(controller=self)
        self.head = Head(controller=self)
        self.arm = Arm(controller=self)
        # TODO based on model decide which subsystems to initialize