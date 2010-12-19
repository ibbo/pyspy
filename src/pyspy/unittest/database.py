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

"""Unit tests for pyspy.database"""
import pyspy
import pyspy.database
from pyspy.constants import *

import unittest
import pygame

class DatabaseTest(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        self.db = pyspy.database.DictDatabase()
        self.image = pyspy.images.SpyImage(pyspy.images.IMAGE_SIZE,
                'test_image')
        self.mask = pyspy.images.ImageMask('', pyspy.levels.EASY, 'test_clue')

    def test_add_image(self):
        """Test adding an image to the database"""
        self.db.add_image(self.image)

    def test_get_image(self):
        """Test retrieving an image from the database"""
        self.db.add_image(self.image)
        image_retrieved = self.db.get_image(self.image.name)
        self.assertEqual(self.image, image_retrieved,
            """The image returned from the database was not
            equal to the image put in the database""")

    def test_fail_get(self):
        """Test getting a non-existent item from the database"""
        try:
            self.db.get_image('No image')
        except pyspy.database.DatabaseError:
            # We expect this to throw a database error
            pass

    def test_add_mask(self):
        """Test adding a mask to the database"""
        self.db.add_mask(self.mask, self.image.name)

    def test_get_mask_by_clue(self):
        """Test getting a mask from the database by clue"""
        self.db.add_mask(self.mask, self.image.name)
        mask = self.db.get_mask(self.image.name, self.mask.clue)
        self.assertEqual(self.mask, mask,
            """The mask returned from the database was not correct""")

    def test_get_masks_by_difficulty(self):
        """Test getting a list of masks for a level by difficulty"""
        parent = 'test_image'
        masks = [pyspy.images.ImageMask('', pyspy.levels.EASY,
                'test_clue1'),
                pyspy.images.ImageMask('', pyspy.levels.EASY,
                    'test_clue2'),
                pyspy.images.ImageMask('', pyspy.levels.HARD,
                    'test_clue3')]
        [self.db.add_mask(mask, parent) for mask in masks]
        retrieved_masks = self.db.get_mask(parent, 
                difficulty=pyspy.levels.EASY)
        self.assertEqual(2, len(retrieved_masks))
        self.assertTrue(retrieved_masks[0] == masks[0])
        # Now try and get a MEDIUM difficulty mask
        self.assertTrue(
            self.db.get_mask(parent, difficulty=pyspy.levels.MEDIUM) == [])

class DatabaseBuilderTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.db = pyspy.database.DictDatabase()
        self.db_builder = pyspy.database.DatabaseBuilder()
        self.image = pyspy.images.SpyImage(pyspy.images.IMAGE_SIZE,
                'test_image')
        self.masks = [pyspy.images.ImageMask('', pyspy.levels.EASY,
                'test_clue1'),
                pyspy.images.ImageMask('', pyspy.levels.EASY,
                    'test_clue2'),
                pyspy.images.ImageMask('', pyspy.levels.HARD,
                    'test_clue3')]

    def test_put_level(self):
        """Test putting level into the database"""
        self.db_builder.put_level(self.db, self.image, self.masks)
        image = self.db.get_image('test_image')
        self.assertEqual(self.image, image)
        mask = self.db.get_mask('test_image', 'test_clue1')
        self.assertEqual(self.masks[0], mask)

if __name__ == "__main__":
    unittest.main()
