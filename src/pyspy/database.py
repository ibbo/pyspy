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

"""Code to interact with a database of pySpy images"""
import pyspy
import pyspy.levels
from pyspy.constants import *

def load_database_from_file(db, level_name):
    db_builder = pyspy.database.DatabaseBuilder()
    if pyspy.levels.checkLevel(level_name):
        image = pyspy.images.SpyImage(pyspy.images.IMAGE_SIZE, level_name)
        masks, has_spythis = pyspy.levels.getMasksForLevel(level_name)
        db_builder.put_level(db, image, masks)


class Database:
    """Abstract class for pyspy databases"""
    def __init__(self):
        pass

    def add_image(self, image):
        pass

    def get_image(self, image_name):
        pass

    def add_mask(self, mask, parent):
        pass

    def get_mask(self, image_name, clue='', difficulty=-1):
        pass

    def get_num_masks(self, image_name):
        pass

class DictDatabase(Database):
    """A simple database which stores the images in a dictionary"""
    def __init__(self):
        self.images = {}
        self.masks_by_parent = {}
        self.masks_by_clue = {}
        self.masks_by_difficulty = {}

    def add_image(self, image):
        """Add an image to the database"""
        self.images[image.name] = image

    def get_image(self, image_name):
        """Retrieve an image from the database"""
        if image_name is None:
            return self.images.values()
        try:
            return self.images[image_name]
        except KeyError:
            reason = "Image: '%s' is not in database" %(image_name)
            raise DatabaseError("DictDatabase:get_image", reason)

    def add_mask(self, mask, parent):
        """Add a mask to the database"""
        if not self.masks_by_clue.has_key(parent):
            self.masks_by_clue[parent] = {mask.clue: mask}
            self.masks_by_parent[parent] = [mask]
        else:
            self.masks_by_clue[parent][mask.clue] = mask
            self.masks_by_parent[parent].append(mask)
        if not self.masks_by_difficulty.has_key(mask.level):
            self.masks_by_difficulty[mask.level] = [mask]
        else:
            self.masks_by_difficulty[mask.level].append(mask)

    def get_mask(self, image_name, clue='', difficulty=-1):
        """Get a mask from the database, by clue or difficulty"""
        if clue != '':
            try:
                return self.masks_by_clue[image_name][clue]
            except KeyError:
                reason = "No mask found for image: %s, with clue: %s" \
                    %(image_name, clue)
                raise DatabaseError("DictDatabase:get_mask", reason)
        elif difficulty >= 0:
            try:
                return self.masks_by_difficulty[difficulty]
            except KeyError:
                # If we have no masks at that difficulty we don't want to
                # error, we simply return an empty list.
                return []
        else:
            return self.masks_by_parent[image_name]

    def get_num_masks(self, image_name):
        if self.masks_by_clue.has_key(image_name):
            return len(self.masks_by_clue[image_name].keys())
        else:
            return 0


class DatabaseError(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        return repr(self.expr + ", " + self.msg)

class DatabaseBuilder:
    """A class for building a pyspy database from scratch"""
    def put_level(self, db, image, masks):
        db.add_image(image)
        for mask in masks:
            db.add_mask(mask, image.name)
