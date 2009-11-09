import os
import sys
sys.path.append(os.path.split(os.getcwd())[0])
import pyspy

def update():
    """update() - Downloads updates for pyspy levels if available

    Returns false if no updates were available"""
    updates = pyspy.levels.checkForUpdates()
    if updates:
        pyspy.levels.downloadUpdates(updates)
        for i in updates:
            pyspy.levels.generateLevel(pyspy.utilities.strip_ext(i))
        return True
    else:
        return False

if __name__ == '__main__':
    update()
