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

from distutils.core import setup

setup(name='pyspy',
      version='1.1a1',
      description='An "I Spy" game',
      author='Thomas Ibbotson',
      author_email='thomas.ibbotson@gmail.com',
      url='http://launchpad.net/pyspy',
      packages = ['pyspy', 'pyspy.original', 'pyspy.spythis'],
      package_dir={'pyspy': 'src/pyspy', 'pyspy.original': 'src/pyspy/original', 'pyspy.spythis': 'src/pyspy/spythis'}
     )
