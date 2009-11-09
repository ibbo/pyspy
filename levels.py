#!/usr/bin/python
import sys
import os
import re
import shutil

def generateLevel(level, path='levels'):
    #TODO: Make this check for other versions of the Gimp
    if not os.path.exists(os.path.join(os.environ['HOME'], '.gimp-2.6')):
        #FIXME: This should be more than just an "Exception"
        raise Exception, "Gimp installation not found"
    
    layerScriptPath = os.path.join(os.environ['HOME'], '.gimp-2.6', \
                                    'plug-ins', 'gimpSaveLayers.py')
    if not os.path.exists(layerScriptPath):
        shutil.copy(os.path.join(path,'gimpSaveLayers.py'), layerScriptPath)
    
    generateScriptPath = os.path.join(os.environ['HOME'], '.gimp-2.6', \
                                    'scripts', 'generate_levels.scm')
    if not os.path.exists(generateScriptPath):
        shutil.copy(os.path.join(path,'generate_levels.scm'), generateScriptPath)
    
    os.system("gimp -i -b '(generate-levels \"%s.xcf\")' -b '(gimp-quit 0)'"
                %(os.path.join(path,level)))

if __name__ == '__main__':
    generateLevel('*')
