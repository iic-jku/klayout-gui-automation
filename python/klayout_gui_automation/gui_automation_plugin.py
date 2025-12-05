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
from pathlib import Path
import traceback
from typing import *

import pya

from klayout_plugin_utils.debugging import debug, Debugging
from klayout_plugin_utils.event_loop import EventLoop
from klayout_plugin_utils.str_enum_compat import StrEnum

from klayout_gui_automation.log_event_handler import LogEventHandler
from klayout_gui_automation.low_level_event_combiner import LowLevelEventCombiner
from klayout_gui_automation.high_level_event_combiner import HighLevelEventCombiner
from klayout_gui_automation.event_recorder import *
from klayout_gui_automation.event_replayer import *

class GUIAutomationPluginState(StrEnum):
    STOPPED = 'stopped'
    RECORDING = 'recording'


class GUIAutomationPluginFactory(pya.PluginFactory):
    def __init__(self):
        super().__init__()
                
        try:
            self._record_tray: Optional[pya.QSystemTrayIcon] = None
            self._state: GUIAutomationPluginState = GUIAutomationPluginState.STOPPED
            
            self._recorded_event_handler = HighLevelEventCombiner(LowLevelEventCombiner(LogEventHandler()))
            self._recorder = EventRecorder(self._recorded_event_handler)
            self._replayer = EventReplayer()
            
            self.has_tool_entry = False
            self.register(-1000, "gui_automation", "GUI Automation")
            
            self.install_system_tray_icons()
        except Exception as e:
            print("GUIAutomationPluginFactory.ctor caught an exception", e)
            traceback.print_exc()
    
    def menu_activated(self, symbol: str) -> bool:
        if Debugging.DEBUG:
            debug(f"GUIAutomationPluginFactory.menu_activated: symbol={symbol}")
            
    @property
    def view(self) -> pya.LayoutView:
        return pya.LayoutView.current()
            
    @property
    def cell_view(self) -> pya.CellView:
        return pya.CellView.active()

    @property
    def layout(self) -> pya.Layout:
        return self.cell_view.layout()

    @property
    def tech(self) -> pya.Technology:
        return self.layout.technology()

    @property
    def state(self) -> GUIAutomationPluginState:
        return self._state
        
    @state.setter
    def state(self, state: GUIAutomationPluginState):
        if Debugging.DEBUG:
            debug(f"GUIAutomationPluginFactory.state: Transitioning from {self._state.value} to {state.value}")
        self._state = state
    
        match self.state:
            case GUIAutomationPluginState.STOPPED:
                self.stop_recording()
                
            case GUIAutomationPluginState.RECORDING:
                self.start_recording()
    
    def start_recording(self):
        if Debugging.DEBUG:
            debug("GUIAutomationPluginFactory.start_recording")
        
        self._recorder.start()
        
    def stop_recording(self):
        if Debugging.DEBUG:
            debug("GUIAutomationPluginFactory.stop_recording")

        self._recorder.stop()

    def install_system_tray_icons(self):
        if Debugging.DEBUG:
            debug("GUIAutomationPluginFactory.install_system_tray_icons")
        
        mw = pya.MainWindow.instance()
        record_icon = pya.QIcon(':breakpoint_16px')
        stop_icon = pya.QIcon(':pause_16px')
        tray_icon = pya.QSystemTrayIcon(mw)
        
        def toggle_recording():
            if Debugging.DEBUG:
                debug(f"GUIAutomationPluginFactory.install_system_tray_icons: Toggle recording")
            
            if tray_icon.icon.cacheKey() == record_icon.cacheKey():
                tray_icon.setIcon(stop_icon)
                tray_icon.setToolTip("Stop Recording")
                self.state = GUIAutomationPluginState.RECORDING
            else:
                tray_icon.setIcon(record_icon)
                tray_icon.setToolTip("Start Recording")
                self.state = GUIAutomationPluginState.STOPPED
        
        tray_icon.activated.connect(toggle_recording)
        
        tray_icon.setIcon(record_icon)
        tray_icon.setToolTip("Start Recording")
        tray_icon.show()

        self._record_tray_icon = tray_icon   # keep alive

    def clear_menu(self):
        if Debugging.DEBUG:
            debug("GUIAutomationPluginFactory.clear_menu")
                
        mw = pya.MainWindow.instance()
        menu = mw.menu()
        menu.clear_menu("macros_menu.test_automation_group")
    
    def setup(self):
        try:
            if Debugging.DEBUG:
                debug("GUIAutomationPluginFactory.setup")
        except Exception as e:
            print("GUIAutomationPluginFactory.setup caught an exception", e)
            traceback.print_exc()            
            
    def reset_menu(self):
        self.clear_menu()

    def configure(self, name: str, value: str) -> bool:
        if Debugging.DEBUG:
            debug(f"GUIAutomationPluginFactory.configure, name={name}, value={value}")
            
        return False

    def stop(self):
        if Debugging.DEBUG:
            debug(f"GUIAutomationPluginFactory.stop")
    
        self.state = GUIAutomationPluginState.STOPPED
    
        if self._record_tray_icon is not None:
            self._record_tray_icon.hide()
            self._record_tray_icon.deleteLater()
            self._record_tray_icon = None
            
