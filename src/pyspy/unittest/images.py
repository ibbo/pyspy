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

import pyspy
import pyspy.images

import unittest

class MaskListTest(unittest.TestCase):

    def setUp(self):
        self.level_name = 'test_image'
        # Populate a database with test items
        db = pyspy.database.DictDatabase()
        db_builder = pyspy.database.DatabaseBuilder()
        self.image = pyspy.images.SpyImage(pyspy.images.IMAGE_SIZE,
                 self.level_name)
        self.masks = [pyspy.images.ImageMask('', pyspy.levels.EASY,
                'test_clue1'),
                pyspy.images.ImageMask('', pyspy.levels.EASY,
                    'test_clue2'),
                pyspy.images.ImageMask('', pyspy.levels.HARD,
                    'test_clue3')]
        db_builder.put_level(db, self.image, self.masks)
        # Create a masklist object for the tests
        self.masklist = pyspy.images.MaskList(db)
    
    def test_load_masks(self):
        self.masklist.load_masks(self.level_name)

    def test_get_mask(self):
        masks = self.masklist.get_mask(self.level_name, pyspy.levels.EASY)
        self.assertTrue(masks[0] == self.masks[0])
