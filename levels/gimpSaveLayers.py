#!/usr/bin/python
from gimpfu import *
import sys, os
#TODO: Find a better way of doing this!
sys.path.append(os.path.join('/','home','ibbo','pySpy','images'))
import imageList as il

def parse_layer_name(layer):
    result = layer.name.split(':')
    if len(result) > 1:
        return result[0], int(result[1])
    else:
        return result[0], None

def python_save_layers(timg, tdrawable):
    for l in timg.layers:
        name, level = parse_layer_name(l)
        imageFile = os.path.split(timg.filename)
        imageName = imageFile[1][0:-4]
        if name == "Background":
            filename = imageName+'.png'
        else:
            filename = imageName+'_'+name.replace(' ','_')+'.png'
            il.addClue(imageName, name.replace(' ','_'), level, imageFile[0])
        pdb.file_png_save_defaults(timg, l, filename, filename)

register(
        "python_fu_save_layers",
        "Save the layers in the image (as png)",
        "Save the layers in the image (as png)",
        "Thomas Ibbotson",
        "Thomas Ibbotson",
        "2009",
        "<Image>/File/Save Layers",
        "RGB*",
        [],
        [],
        python_save_layers)

main()
