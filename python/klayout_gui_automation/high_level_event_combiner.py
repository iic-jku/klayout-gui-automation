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


class HighLevelEventCombiner(EventHandler):
    def __init__(self, delegate: EventHandler):
        self.delegate = delegate
        
        self.previous_events: List[Event] = []
    
    def flush(self):
        for e in self.previous_events:
            self.delegate.handle_event(e)
        self.previous_events = []

    @property
    def previous_event(self) -> Optional[Event]:
        if len(self.previous_events) == 0:
            return None
        return self.previous_events[-1]
    
    def needs_flush(self, event: Event) -> bool:
        p = self.previous_event
        if p is None:
            return False
            
        if p.target != event.target:
            return True
            
        p_kind = p.kind if p else None
        p_event_type = p.event.type if p else pya.QEvent.None_
        match (p_kind, event.kind):
            case (Event.Kind.KEY_EVENT, Event.Kind.KEY_EVENT):  # we can merge keyDown/keyUp into TypeEvents
                match (p_event_type, event.event.type):
                    case (pya.QEvent.None_, pya.QEvent.KeyPress):
                        return False
                    
                    case (pya.QEvent.KeyPress, pya.QEvent.KeyRelease):
                        return False
                
                return True
                        
            case (Event.Kind.TYPE_EVENT, Event.Kind.KEY_EVENT):
                return False
        
            case (Event.Kind.MOUSE_EVENT, Event.Kind.MOUSE_EVENT):  # TODO
                match (p_event_type, event.event.type):
                    case (pya.QEvent.None_, pya.QEvent.MouseButtonPress):
                        return False
                
                    case (pya.QEvent.MouseButtonPress, pya.QEvent.MouseButtonRelease):
                        return False
                
                # return False if mergeable
                return True

        return True
    
    def _try_combine_key_event(self, event: Event) -> bool:
        # see if we can combine
        if event.kind != Event.Kind.KEY_EVENT:
            return False
        
        p = self.previous_event
        p_kind = p.kind if p else None
        p_event_type = p.event.type if p else pya.QEvent.None_
        
        match (p_kind, event.kind):
            case (Event.Kind.KEY_EVENT, Event.Kind.KEY_EVENT):  # we can merge keyDown/keyUp into TypeEvents
                match (p_event_type, event.event.type):
                    case (pya.QEvent.None_, pya.QEvent.KeyPress):
                        # delay emitting this event, as we can combine
                        self.previous_events.append(event)
                        return True
                        
                    case (pya.QEvent.KeyPress, pya.QEvent.KeyRelease):
                        self.previous_events.pop()
                        p = self.previous_event
                        if p is None:
                            te = Event(kind=Event.Kind.TYPE_EVENT,
                                       target=event.target,
                                       event=TypeEvent(text=event.event.text))
                            self.previous_events.append(te)
                        elif p.kind == Event.Kind.TYPE_Event:
                            p.text += event.event.text
                        # delay emitting this event, as we can combine
                        return True
                
            case (Event.Kind.TYPE_EVENT, Event.Kind.KEY_EVENT):
                # delay emitting this event, as we can combine
                self.previous_events.append(event)
                return True
        
        return False
    
    def _try_combine_mouse_event(self, event: Event) -> bool:
        # see if we can combine
        if event.kind != Event.Kind.MOUSE_EVENT:
            return False
        
        p = self.previous_event
        p_kind = p.kind if p else None
        p_event_type = p.event.type if p else pya.QEvent.None_
        
        match (p_kind, event.kind):
            case (Event.Kind.MOUSE_EVENT, Event.Kind.MOUSE_EVENT):  # we can merge keyDown/keyUp into TypeEvents
                match (p_event_type, event.event.type):
                    case (pya.QEvent.None_, pya.QEvent.MouseButtonPress):
                        # delay emitting this event, as we can combine
                        self.previous_events.append(event)
                        return True
                        
                    case (pya.QEvent.MouseButtonPress, pya.QEvent.MouseButtonRelease):
                        self.previous_events.pop()
                        p = self.previous_event
                        if p is None:
                            te = Event(kind=Event.Kind.CLICK_EVENT,
                                       target=event.target,
                                       event=TypeEvent(text=event.event.text))
                            self.previous_events.append(te)
                        elif p.kind == Event.Kind.TYPE_Event:
                            p.text += event.event.text
                        # delay emitting this event, as we can combine
                        return True
                
        return False

    def handle_event(self, event: Event):
        if Debugging.DEBUG:
            debug(f"HighLevelEventCombiner.handle_event: enter!")

        if self.needs_flush(event):
            if Debugging.DEBUG:
                debug(f"HighLevelEventCombiner.handle_event: need flush!")
            
            self.flush()
            self.delegate.handle_event(event)
            return
        
        if self._try_combine_key_event(event):
            if Debugging.DEBUG:
                debug(f"HighLevelEventCombiner.handle_event: merging key event worked!")
            return
        elif self._try_combine_mouse_event(event):
            if Debugging.DEBUG:
                debug(f"HighLevelEventCombiner.handle_event: merging key event worked!")
            return
        else:           
            if Debugging.DEBUG:
                debug(f"HighLevelEventCombiner.handle_event: fallback, call delegate!")
            self.delegate.handle_event(event)
    