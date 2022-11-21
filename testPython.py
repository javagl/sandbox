#!/usr/bin/env python
import json
import os

def generateFile():
    contents = {}
    fileList = [f for f in os.listdir(".") if f.endswith(".md")]
    for f in fileList:
      contents[f] = os.path.getsize(f);
      
    with open("testPythonOutput.json", "w") as f:
        json.dump(contents, f, indent=2, sort_keys=True)
        f.write("\n")

generateFile();
