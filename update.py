import os
import sys
sys.path.append(os.path.split(os.getcwd())[0])
import pyspy

if __name__ == '__main__':
    updates = pyspy.levels.checkForUpdates()
    pyspy.levels.downloadUpdates(updates)
    for i in updates:
        pyspy.levels.generateLevel(pyspy.utilities.strip_ext(i))
