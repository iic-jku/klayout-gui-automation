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


class EventRecorder(pya.QObject):
    def __init__(self, event_handler: EventHandler):
        self._event_handler = event_handler
        self._recording = False

    def start(self):
        if Debugging.DEBUG:
             debug("EventRecorder.start")

        if self._recording:
            if Debugging.DEBUG:
                 debug(f"EventRecorder.start: already in state 'recording', ignoring…")
            return
        self._recording = True
        
        app = pya.Application.instance()
        app.installEventFilter(self)
        
    def stop(self):
        if not self._recording:
            if Debugging.DEBUG:
                 debug(f"EventRecorder.stop: already in state 'stopped', ignoring…")
            return
        self._recording = False

        if Debugging.DEBUG:
             debug("EventRecorder.stop")
    
    
        app = pya.Application.instance()
        app.removeEventFilter(self)
    
    def action(self, action: pya.QAction):
        if not self._recording:
            return
        
        if Debugging.DEBUG:
             debug(f"EventRecorder.action")
        
        self._event_handler.handle_action_event(action.parent(), action.objectName())
        

    @staticmethod
    def is_modifier_key(event: pya.QKeyEvent) -> bool:
        match event.key():
            case pya.Qt.Key_Control | pya.Qt.Key_Alt | pya.Qt.Key_Shift:
                return True
            case _:
                return False

    def probe(self, widget: pya.QWidget, data: Any):
        if self._recording:
            if Debugging.DEBUG:
                 debug(f"EventRecorder.probe")
        
            self.event_handler.handle_probe_event(widget, data)

    def probe_qtreeview(self, tv: pya.QTreeView) -> Any:
        raise NotImplementedError("TODO")

    def probe_qlineedit(self, le: pya.QLineEdit) -> Any:
        return le.text
        
    def probe_qtextedit(self, te: pya.QTextEdit) -> Any:
        vt = []
        lines = te.toPlainText().split('\n')
        for line in lines:
            vt.push(line)
        return vt 
    
    def probe_qspinbox(self, sb: pya.QSpinBox) -> Any:
        return sb.value
        
    def probe_qcheckbox(self, cb: pya.QCheckBox) -> Any:
        return cb.checked
        
    def probe_qcombobox(self, cmb: pya.QComboBox) -> Any:
        return cmb.lineEdit().text
        
    def probe_qlistview(self, tv: pya.QListView) -> Any:
        raise NotImplementedError("TODO")
        
    def probe_qradiobutton(self, rb: pya.QRadioButton) -> Any:
        return rb.checked

    def probe_qpushbutton(self, pb: pya.QPushButton) -> Any:
        if not pb.icon.isNull():
            raise NotImplementedError("TODO")
        return pb.text

    def probe_std(self, widget: pya.QWidget) -> Any:
        if isinstance(widget, pya.QTreeView) or isinstance(widget, pya.QTreeView_Native):
            self.probe_qtreeview(widget)
        elif isinstance(widget, pya.QLineEdit) or isinstance(widget, pya.QLineEdit_Native):
            self.probe_qlineedit(widget)
        elif isinstance(widget, pya.QTextEdit) or isinstance(widget, pya.QTextEdit_Native):
            self.probe_qtextedit(widget)
        elif isinstance(widget, pya.QSpinBox) or isinstance(widget, pya.QSpinBox_Native):
            self.probe_qspinbox(widget)
        elif isinstance(widget, pya.QCheckBox) or isinstance(widget, pya.QCheckBox_Native):
            self.probe_qcheckbox(widget)
        elif isinstance(widget, pya.QComboBox) or isinstance(widget, pya.QComboBox_Native):
            self.probe_qcombobox(widget)
        elif isinstance(widget, pya.QListView) or isinstance(widget, pya.QListView_Native):
            self.probe_qlistview(widget)
        elif isinstance(widget, pya.QRadioButton) or isinstance(widget, pya.QRadioButton_Native):
            self.probe_qradiobutton(widget)
        elif isinstance(widget, pya.QPushButton) or isinstance(widget, pya.QPushButton_Native):
            self.probe_qpushbutton(widget)
        else:
            return None
        
    def is_valid_widget(self, widget: pya.QWidget) -> bool:
        if isinstance(widget, pya.QToolBar) or isinstance(widget, pya.QToolBar_Native)\
           or isinstance(widget, pya.QMenuBar) or isinstance(widget, pya.QMenuBar_Native)\
           or isinstance(widget, pya.QMenu) or isinstance(widget, pya.QMenu_Native):
           return False
        
        if widget.parentWidget() is None:
            if isinstance(widget, pya.QDialog) or isinstance(widget, pya.QDialog_Native)\
                or isinstance(widget, pya.QMainWindow) or isinstance(widget, pya.QMainWindow_Native):
                return True
            else:
                return False
        
        return self.is_valid_widget(widget.parentWidget())
    
    def eventFilter(self, watched_object: pya.QObject, event: pya.QEvent) -> bool:
        try:
            # NOTE: don't log, its a hotspot
            # if Debugging.DEBUG:
            #    debug(f"EventRecorder.eventFilter: watched_object={watched_object}, eventType={event.type()}")
    
            # only handle events that targeted towards widgets
            if not watched_object.isWidgetType():
                return False
            
            widget: pya.QWidget = watched_object
    
            # if Debugging.DEBUG:
            #    debug(f"EventRecorder.eventFilter: widget={widget} eventType={event.type()}")
    
            # only log key events that are targeted towards widgets that do not have the focus
            # this propagation of events is done automatically on replay in the same fashion.
            if isinstance(event, pya.QKeyEvent) and not widget.hasFocus():
                return False
            
            # do not log propagation events for mouse events
            if isinstance(event, pya.QMouseEvent) and not event.spontaneous():
                return False
    
            match event.type():
                case pya.QEvent.KeyPress | pya.QEvent.KeyRelease:
                    if Debugging.DEBUG:
                        debug(f"EventRecorder.eventFilter: event.type()={event.type()}")
                    
                    if self.is_modifier_key(event):
                        return False

                    self._event_handler.handle_key_event(widget, event)
                    
                case pya.QEvent.MouseButtonDblClick |\
                     pya.QEvent.MouseButtonPress |\
                     pya.QEvent.MouseButtonRelease:
                    mouse_event: pya.QMouseEvent = event
                    
                    # detect probe event
                    if (
                       event.type() == pya.QEvent.MouseButtonPress
                       and mouse_event.button() == pya.Qt.LeftButton
                       and (mouse_event.modifiers & (pya.Qt.AltModifier | pya.Qt.ControlModifier))
                    ):
                        probe_event = pya.QEvent(pya.QEvent.MaxUser)
                        probe_event.ignore()
                        
                        app = pya.QApplication.instance()
                        
                        next_widget = widget
                        while next_widget is not None:
                            app.sendEvent(next_widget, probe_event)
                            if probe_event.isAccepted():
                                if Debugging.DEBUG:
                                     debug(f"EventRecorder.eventFilter: probed widget {next_widget}")
                                return True
                            next_widget = next_widget.parentWidget()
                        
                        # if there is no special handling, try the default impl
                        next_widget = widget
                        while next_widget is not None:
                            p = self.probe_std(next_widget)
                            if p is not None:
                                self.probe(next_widget, p)
                                if Debugging.DEBUG:
                                     debug(f"EventRecorder.eventFilter: probed widget {next_widget}")
                                return True
                            next_widget = next_widget.parentWidget()
                        
                        return True  # eat probe events
                    elif self.is_valid_widget(widget):
                        self._event_handler.handle_mouse_event(widget, event)
                    else:
                        if Debugging.DEBUG:
                            debug(f"EventRecorder.eventFilter: mouse event, but not a valid widget: {widget}")
                case pya.QEvent.MouseMove:
                    if self.is_valid_widget(widget):
                        self._event_handler.handle_mouse_event(widget, event)
                case pya.QEvent.Resize:
                    if widget.parentWidget() is None and self.is_valid_widget(widget):
                        self._event_handler.handle_resize_event(widget, event)
        except Exception as e:
            app = pya.Application.instance()
            app.removeEventFilter(self)

            print("EventRecorder.ctor caught an exception", e)
            traceback.print_exc()
            
        return False
