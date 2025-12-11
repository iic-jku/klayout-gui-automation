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

from klayout_gui_automation.event import Event
from klayout_gui_automation.event_handler import EventHandler


HOT_SPOT_DEBUGGING = False


class LowLevelEventCombiner(EventHandler):
    def __init__(self, delegate: EventHandler):
        self.delegate = delegate
        
        self.previous_event: Optional[Event] = None
    
    def flush(self):
        if self.previous_event is not None:
            self.delegate.handle_event(self.previous_event)
        self.previous_event = None
    
    def needs_flush(self, event: Event) -> bool:
        if self.previous_event is None:
            return False
    
        match event.kind:
            case Event.Kind.MOUSE_EVENT | Event.Kind.RESIZE_EVENT:
                if self.previous_event.target != event.target:
                    if Debugging.DEBUG and HOT_SPOT_DEBUGGING:
                        debug(f"LowLevelEventCombiner.needs_flush: yes (different target)!")
                    return True
                elif self.previous_event.kind != event.kind:
                    if Debugging.DEBUG and HOT_SPOT_DEBUGGING:
                        debug(f"LowLevelEventCombiner.needs_flush: yes (different event kind)!")
                    return True
        if event.kind == Event.Kind.RESIZE_EVENT:
            return False
        elif event.kind == Event.Kind.MOUSE_EVENT\
            and event.event.type == pya.QEvent.MouseMove:
            if self.previous_event.event.type != event.event.type\
                or self.previous_event.event.button != event.event.button\
                or self.previous_event.event.buttons != event.event.buttons\
                or self.previous_event.event.modifiers != event.event.modifiers:
                if Debugging.DEBUG and HOT_SPOT_DEBUGGING:
                    debug(f"LowLevelEventCombiner.needs_flush: yes (different event properties)!")
                return True
            return False
        
        if Debugging.DEBUG and HOT_SPOT_DEBUGGING:
            debug(f"LowLevelEventCombiner.needs_flush: yes (no matching type combinations)!")
        return True
    
    def handle_event(self, event: Event):
        if Debugging.DEBUG and HOT_SPOT_DEBUGGING:
            debug(f"LowLevelEventCombiner.handle_event: enter!")
            
        if self.needs_flush(event):
            self.flush()
            self.delegate.handle_event(event)
            return
        
        # see if we can combine
        if event.kind == Event.Kind.MOUSE_EVENT and event.event.type == pya.QEvent.MouseMove:
            if self.previous_event is None:
                # delay emitting this event, as we can combine moves
                self.previous_event = event
                return
            else: # needs_flush()==False guarantees this is also a mergeable QMouseMoveEvent
                delta = event.event.global_pos - self.previous_event.event.global_pos
                self.previous_event.event.pos += delta
                self.previous_event.event.global_pos += delta
                return
        elif event.kind == Event.Kind.RESIZE_EVENT:
            if self.previous_event is None:
                # delay emitting this event, as we can combine moves
                self.previous_event = event
                return
            else: # needs_flush()==False guarantees this is also a mergeable QMouseMoveEvent
                self.previous_event.event.new_size = event.event.new_size
                return
        
        if Debugging.DEBUG and HOT_SPOT_DEBUGGING:
            debug(f"LowLevelEventCombiner.handle_event: fallback, call delegate!")
        
        self.delegate.handle_event(event)
