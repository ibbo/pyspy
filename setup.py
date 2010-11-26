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
import glob
import os,sys

pathFile = open(os.path.join('src','pyspy','pathDef.py'), 'w')
pathFile.write("CURSOR_DIR = '%s/share/pyspy/cursors'\n" % sys.prefix)
pathFile.write("IMAGE_DIR = '%s/share/pyspy/images'\n" % sys.prefix)
pathFile.write("MUSIC_DIR = '%s/share/pyspy/music'\n" % sys.prefix)
pathFile.write("SOUND_DIR = '%s/share/pyspy/sounds'\n" % sys.prefix)
pathFile.write("LEVEL_DIR = '%s/share/pyspy/levels'\n" % sys.prefix)
pathFile.write("FONT_DIR = '%s/share/pyspy/fonts'\n" % sys.prefix)
pathFile.close()

setup(name='pyspy',
      version='1.1-alpha2',
      description='An "I Spy" game',
      author='Thomas Ibbotson',
      author_email='thomas.ibbotson@gmail.com',
      url='http://launchpad.net/pyspy',
      packages = ['pyspy', 'pyspy.original', 'pyspy.spythis'],
      package_dir={'pyspy': 'src/pyspy',
                   'pyspy.original': 'src/pyspy/original',
                   'pyspy.spythis': 'src/pyspy/spythis'},
      scripts=['src/scripts/update.py', 'src/scripts/pyspy'],
      data_files=[
          ('share/pyspy/cursors', glob.glob(os.path.join('cursors','*.xbm'))),
          ('share/pyspy/fonts', glob.glob(os.path.join('fonts','*.ttf'))),
          ('share/pyspy/images', glob.glob(os.path.join('images','*.png'))),
          ('share/pyspy/levels', glob.glob(os.path.join('levels','*.png'))),
          ('share/pyspy/music', glob.glob(os.path.join('music','*.mid'))),
          ('share/pyspy/sounds', glob.glob(os.path.join('sounds','*.wav'))),
          ]
     )
