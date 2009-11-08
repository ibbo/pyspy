#!/usr/bin/python
import sys
import os
import re
import shutil

#TODO: Make this check for other versions of the Gimp
if not os.path.exists(os.path.join(os.environ['HOME'], '.gimp-2.6')):
    #FIXME: This should be more than just an "Exception"
    raise Exception, "Gimp installation not found"

layerScriptPath = os.path.join(os.environ['HOME'], '.gimp-2.6', \
                                'plug-ins', 'gimpSaveLayers.py')
if not os.path.exists(layerScriptPath):
    shutil.copy('gimpSaveLayers.py', layerScriptPath)

generateScriptPath = os.path.join(os.environ['HOME'], '.gimp-2.6', \
                                'scripts', 'generate_levels.scm')
if not os.path.exists(generateScriptPath):
    shutil.copy('generate_levels.scm', generateScriptPath)

os.system("gimp -i -b '(generate-levels \"*.xcf\")' -b '(gimp-quit 0)'")
