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

from __future__ import annotations
from dataclasses import dataclass
from typing import *

import pya

from klayout_plugin_utils.str_enum_compat import StrEnum

from klayout_gui_automation.widget_path import WidgetPath

#---------------------------------------------------------------------------------
#------------------------------  Low Level Events   ------------------------------
#---------------------------------------------------------------------------------

@dataclass
class MouseEvent:
    type: pya.QEvent.Type
    pos: pya.QPoint
    global_pos: pya.QPoint
    button: pya.Qt.MouseButton
    buttons: pya.Qt_QFlags_MouseButton
    modifiers: pya.Qt_QFlags_KeyboardModifier
    
    @classmethod
    def from_qt(cls, e: pya.QMouseEvent) -> MouseEvent:
        return MouseEvent(
            type=e.type(),
            pos=e.pos(),
            global_pos=e.globalPos(),
            button=e.button(),
            buttons=e.buttons(),
            modifiers=e.modifiers
        )


@dataclass
class KeyEvent:
    type: pya.QEvent.Type
    key: int
    text: str
    modifiers: pya.Qt_QFlags_KeyboardModifier
   
    @classmethod
    def from_qt(cls, e: pya.QKeyEvent) -> KeyEvent:
        return KeyEvent(
            type=e.type(),
            key=e.key(),
            text=e.text(),
            modifiers=e.modifiers
        )
   
    
@dataclass
class ResizeEvent:
    type: pya.QEvent.Type
    old_size: pya.QSize
    new_size: pya.QSize

    @classmethod
    def from_qt(cls, e: pya.QResizeEvent) -> ResizeEvent:
        return ResizeEvent(
            type=e.type(),
            old_size=e.oldSize(),
            new_size=e.size()
        )


@dataclass
class ActionEvent:
    action_name: str

    
@dataclass
class ProbeEvent:
    data: Any

#---------------------------------------------------------------------------------
#-----------------------------  High Level Events   ------------------------------
#---------------------------------------------------------------------------------

@dataclass
class TypeEvent:
    text: str

#---------------------------------------------------------------------------------
#------------------------------  Low Level Events   ------------------------------
#---------------------------------------------------------------------------------

@dataclass
class Event:
    class Kind(StrEnum):
        MOUSE_EVENT = 'mouse'
        KEY_EVENT = 'key'
        RESIZE_EVENT = 'resize'
        ACTION_EVENT = 'action'
        PROBE_EVENT = 'probe'
        TYPE_EVENT = 'type'

    kind: Event.Kind
    target: WidgetPath
    event: MouseEvent | KeyEvent | ResizeEvent | ActionEvent | ProbeEvent\
           | TypeEvent


