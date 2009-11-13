#!/usr/bin/python
#    This file is part of pySpy.
#
#   pySpy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pySpy is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pySpy.  If not, see <http://www.gnu.org/licenses/>.
from gimpfu import *
import sys, os
#TODO: Find a better way of doing this!
sys.path.append(os.environ['HOME'])
import pyspy
import pyspy.imageList as il

def parse_layer_name(layer):
    result = layer.name.split(':')
    if len(result) > 1:
        return result[0], int(result[1])
    else:
        return result[0], None

def python_save_layers(timg, tdrawable):
    imageFile = os.path.split(timg.filename)
    imageName = imageFile[1][0:-4]
    levelList = il.getLevelList(imageFile[0])
    levelList = il.clearImage(imageName, levelList)
    height = pdb.gimp_image_height(timg)
    width = pdb.gimp_image_width(timg)
    pdb.gimp_selection_none(timg)
    for l in timg.layers:
        name, level = parse_layer_name(l)
        if name == "Background":
            filename = imageName+'.png'
            filename = os.path.join(imageFile[0], filename)
            pdb.file_png_save_defaults(timg, l, filename, filename)
        else:
            filename = imageName+'_'+name.replace(' ','_')+'.png'
            levelList = il.addClue(
                imageName, name.replace(' ','_'), level, levelList)
            new_img = pdb.gimp_image_new(width, height, 0)
            new_layer = pdb.gimp_layer_new(new_img, width, height, 1,
                    l.name, 100, 0)
            pdb.gimp_image_add_layer(new_img, new_layer, -1)
            pdb.gimp_edit_copy(l)
            pdb.gimp_edit_paste(new_layer, 1)
            display = pdb.gimp_display_new(new_img)
            pdb.gimp_image_convert_indexed(new_img, 0, 3, 2, 1, 0, '')
            filename = os.path.join(imageFile[0], filename)
            pdb.file_png_save_defaults(new_img, new_layer, filename, filename)
            pdb.gimp_display_delete(display)
    il.saveLevelList(levelList, path=imageFile[0])

register(
        "python_fu_save_layers",
        "Save the layers in the image (as png)",
        "Save the layers in the image (as png)",
        "Thomas Ibbotson",
        "Thomas Ibbotson",
        "2009",
        "<Image>/Layer/Save Layers for pySpy",
        "RGB*",
        [],
        [],
        python_save_layers)

main()
