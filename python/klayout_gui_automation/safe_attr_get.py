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

from typing import Any


def safe_attr_get(obj: Any, attr_name: str) -> str:
    """
    Return a string value for attribute or method (call if callable).
    """
    if not hasattr(obj, attr_name):
        return None
    val = getattr(obj, attr_name)
    try:
        if callable(val):
            v = val()
        else:
            v = val
    except Exception:
        # If calling raises, just string-convert the attribute object
        v = val
    if v is None:
        return None
    return str(v)
