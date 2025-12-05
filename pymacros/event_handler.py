# --------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2025 Martin Jan Köhler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later
#--------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import *

import pya


class EventHandler(ABC):
    @abstractmethod
    def handle_action_event(self, widget: pya.QWidget, action_name: str):
        raise NotImplementedError()

    @abstractmethod
    def handle_key_event(self, widget: pya.QWidget, event: pya.QEvent):
        raise NotImplementedError()

    @abstractmethod
    def handle_mouse_event(self, widget: pya.QWidget, event: pya.QEvent):
        raise NotImplementedError()

    @abstractmethod
    def handle_resize_event(self, widget: pya.QWidget, event: pya.QEvent):
        raise NotImplementedError()
    
    @abstractmethod
    def handle_probe_event(self, widget: pya.QWidget, data: Any):
        raise NotImplementedError()
    