import time
import json
import sys
import os

os.system("clear")

global loading
loading = False

import os
import json
import sys

def updateJson(directory):
    dirItems = os.listdir(directory)
    dirData = {}

    for itemnum, item in enumerate(dirItems):
        full_path = os.path.join(directory, item)

        if os.path.isfile(full_path):
            dirData[f"file{itemnum + 1}"] = item
        elif os.path.isdir(full_path):
            dirData[item] = updateJson(full_path)

        percent = (itemnum / len(dirItems)) * 100
        bar = '#' * itemnum + '-' * (len(dirItems) - itemnum)
        sys.stdout.write(f'\r[{bar}] {percent:.2f}% - Processing {directory}')
        sys.stdout.flush()

    return dirData

def main():
    global loading
    fsfile = {}

    while loading:
        curDir = os.getcwd()

        print(f"\nCollecting data for {curDir}...")
        fsfile = {}
        fsfile[curDir] = updateJson(curDir)

        with open('fs.json', 'w') as file:
            json.dump(fsfile, file, indent=4)

        sys.stdout.write(f"\nDumped {curDir}\n")

        loading = False


input("Press enter to begin. ")
print("Recording filesystem from current script location...")
print("")
loading = True
main()
