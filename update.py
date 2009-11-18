#!/usr/bin/python
#    This file is part of pySpy.
#
#    pySpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pySpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySpy.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
sys.path.append(os.path.split(os.getcwd())[0])
import pyspy

def update():
    """update() - Downloads updates for pyspy levels if available

    Returns false if no updates were available"""
    updates = pyspy.levels.checkForUpdates()
    if updates:
        status = pyspy.levels.DownloadStatus()
        pyspy.levels.downloadUpdates(updates, statusObj=status)
        return True
    else:
        return False

if __name__ == '__main__':
    update()
