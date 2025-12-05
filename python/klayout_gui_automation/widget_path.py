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


@dataclass
class WidgetPathEntry:
    widget_name: str
    class_name: str
    
    child_index: Optional[int] = None
    property_filter: Optional[Dict[str, str]] = None

    def xpath(self) -> str:
        s = f"{wcls}"
        if property_filter:  # we prefer the property filter (more robust against GUI changes)
            p = [f"@{k}='{v}'" for k, v in property_filter.items()]
            s += f"[{' and '.join(p)}]"
        elif i > 1:
            s += f"[{i}]"
        return s

@dataclass
class WidgetPath:
    entries: List[WidgetPathEntry]

    @classmethod
    def for_widget(cls, widget: pya.QWidget) -> WidgetPath:
        def is_valid_widget(widget: pya.QWidget) -> bool:
            if isinstance(widget, pya.QDialog) or isinstance(widget, pya.QDialog_Native)\
                or isinstance(widget, pya.QMainWindow) or isinstance(widget, pya.QMainWindow_Native)\
                or isinstance(widget, pya.QWidget) or isinstance(widget, pya.QWidget_Native):
                return True
            return False
            
        def add_entries_for_widget(entries: List[WidgetPathEntry], widget: pya.QWidget):
            wcls = widget.__class__.__name__
    
            property_filter = {}
            
            wn = widget.objectName
            if wn:
                property_filter['oid'] = wn
            
            pw = None
            if 'parentWidget' in dir(widget):
                pw = widget.parentWidget()
            else:
                print(f"{wn} ({wcls}) does not have method parentWidget()")
            
            i = 1
            
            if 'title' in dir(widget):  # title could be a useful property
                property_filter['title'] = widget.title
            
            properties_unique = True
            
            def analyze_siblings_and_self(children: List[pya.QWidget]):
                nonlocal i
                for child in children:
                    if not is_valid_widget(child):
                        continue
                        
                    if child == widget:
                        break
                    elif child.objectName == wn and child.__class__.__name__ == wcls:
                        i += 1
            
            if pw is not None:
                analyze_siblings_and_self(pw.children())
            else:
                analyze_siblings_and_self(pya.QApplication.topLevelWidgets())
            
            e = WidgetPathEntry(widget_name=wn, 
                                class_name=wcls,
                                child_index=None if i == 0 else i,
                                property_filter=property_filter)
            entries.insert(0, e)
            
        entries = []
        add_entries_for_widget(entries, widget)
        return WidgetPath(entries)
    
    def xpath(self) -> str:
        xps = [e.xpath() for e in self.entries]
        return '/'.join(xps)
   
    def __str__(self) -> str:
        return self.xpath()
