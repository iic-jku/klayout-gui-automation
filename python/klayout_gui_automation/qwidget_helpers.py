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


def is_qtoolbar(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QToolBar) or isinstance(widget, pya.QToolBar_Native)

def is_qmenubar(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QMenuBar) or isinstance(widget, pya.QMenuBar_Native)

def is_qmenu(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QMenu) or isinstance(widget, pya.QMenu_Native)

def is_qmainwindow(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QMainWindow) or isinstance(widget, pya.QMainWindow_Native)

def is_qdialog(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QDialog) or isinstance(widget, pya.QDialog_Native)

def is_qtreeview(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QTreeView) or isinstance(widget, pya.QTreeView_Native)
    
def is_qlineedit(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QLineEdit) or isinstance(widget, pya.QLineEdit_Native)
           
def is_qtextedit(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QTextEdit) or isinstance(widget, pya.QTextEdit_Native)

def is_qspinbox(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QSpinBox) or isinstance(widget, pya.QSpinBox_Native)
           
def is_qcheckbox(widget: pya.QWidget) -> bool:
    return isinstance(widget, pya.QCheckBox) or isinstance(widget, pya.QCheckBox_Native)

def is_qcombobox(wigdet: pya.QWidget) -> bool:
    return isinstance(widget, pya.QComboBox) or isinstance(widget, pya.QComboBox_Native)

def is_qlistview(widget: pya.QListView) -> bool:
    return isinstance(widget, pya.QListView) or isinstance(widget, pya.QListView_Native)

def is_qradiobutton(widget: pya.QListView) -> bool:
    return isinstance(widget, pya.QRadioButton) or isinstance(widget, pya.QRadioButton_Native)

def is_qpushbutton(widget: pya.QListView) -> bool:
    return isinstance(widget, pya.QPushButton) or isinstance(widget, pya.QPushButton_Native)

