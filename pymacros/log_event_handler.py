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

from typing import *

import pya

from klayout_plugin_utils.debugging import debug, Debugging

from event_handler import EventHandler


class LogEventHandler(EventHandler):
    def handle_action_event(self, widget: pya.QWidget, action_name: str):
        print(f"LogEventHandler.handle_action_event: widget={widget}, action_name={action_name}")

    def handle_key_event(self, widget: pya.QWidget, event: pya.QEvent):
        print(f"LogEventHandler.handle_key_event: widget={widget}, event={event}")

    def handle_mouse_event(self, widget: pya.QWidget, event: pya.QEvent):
        print(f"LogEventHandler.handle_mouse_event: widget={widget}, event={event}")

    def handle_resize_event(self, widget: pya.QWidget, event: pya.QEvent):
        print(f"LogEventHandler.handle_resize_event: widget={widget}, event={event}")

    def handle_probe_event(self, widget: pya.QWidget, data: Any):
        print(f"LogEventHandler.handle_probe_event: widget={widget}, data={data}")

