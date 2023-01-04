#!/usr/bin/env python
import json
import os

# | Model                                         | Screenshot                                       | Normal Map         | Occlusion Map      | Emissive Map       |
# |-----------------------------------------------|:------------------------------------------------:|:------------------:|:------------------:|:------------------:|
# | [Antique Camera](AntiqueCamera)               | ![](AntiqueCamera/screenshot/screenshot.png)     | :white_check_mark: |                    |                    |



def createModelInfo(name):
    """Creates a model info for the model in the current directory

    Parameters
    ----------
    name: str
        The name of the model

    Returns
    -------
    modelInfo
        The model info
    """    
    modelDirectoryContents = os.listdir(".")
    variantNames = [d for d in modelDirectoryContents if d.startswith("glTF")]
    variants = {}
    for variantName in variantNames:
        fileList = [f for f in os.listdir(variantName)
                        if f.endswith(".glb") or f.endswith(".gltf")]
        if (len(fileList) > 0):
            variants[variantName] = fileList[0]
    if not variants:
        print ("WARNING: no model files found for {}".format(name))

    screenshot = None
    if "screenshot" not in modelDirectoryContents:
        print ("WARNING: no screenshot found for {}".format(name))
    else:
        screenshot = "screenshot/" + [s for s in os.listdir("screenshot") if s.startswith("screenshot.")][0]

    modelInfo = {
        "name": name,
        "variants": variants,
        "screenshot": screenshot
    }
    return modelInfo;

def addModelMetadata(modelInfo):
    """Adds the metadata to the given model info, based on the model metadata file

    Parameters
    ----------
    modelInfo
        The model info
    """    
    modelName = modelInfo["name"]
    try:
        modelMetadataFile = open("model-metadata.json")
    except IOError:
        print ("WARNING: no model-metadata.json file found for {}".format(modelName))
    else:
        with modelMetadataFile:
            modelMetadata = json.load(modelMetadataFile)
            modelInfo["tags"] = modelMetadata["tags"]

def collectModelInfos(directoryName):
    """Collect all model info objects from the given subdirectory

    Parameters
    ----------
    directoryName
        The directory name

    Returns
    -------
    modelInfos
        The model infos dictionary
    """    
    os.chdir(directoryName)
    modelInfos = {}
    for modelName in sorted(os.listdir(".")):
        if not os.path.isdir(modelName):
            continue
        os.chdir(modelName)

        modelInfo = createModelInfo(modelName)
        addModelMetadata(modelInfo)
        modelName = modelInfo["name"]
        modelInfos[modelName] = modelInfo;

        os.chdir("..")
    os.chdir("..")
    return modelInfos


def generateReadmeMarkdown(directoryName):
    """Create a markdown summary of the models in the given directory

    Parameters
    ----------
    directoryName
        The directory name

    Returns
    -------
    md
        The markdown string
    """    

    modelInfos = collectModelInfos(directoryName);
    md = "";
    md += "Example markdown generated from the directory contents and metadata files\n"
    md += "\n"
    md += "| Model | Screenshot | Variants | Tags |\n"
    md += "|-------|:----------:|:--------:|:----:|\n"

    for modelName in modelInfos:
        modelInfo = modelInfos[modelName]
        screenshot = modelInfo["screenshot"]

        variants = modelInfo["variants"]
        variantsKeys = list(variants.keys())

        tags = modelInfo["tags"]

        md += "[" + modelName +"](" + modelName +")"
        md += " | "

        md += "![](" + directoryName + "/" + modelName +"/" + screenshot + ")"
        md += " | "

        md += "<br>".join(str(x) for x in variantsKeys)
        md += " | "

        md += "<br>".join(str(x) for x in tags)
        md += " | "

        md += "\n"

    return md

def generateReadme():
    md = generateReadmeMarkdown("2.0");
    with open("README_generated.md", "w") as readmeFile:
        readmeFile.write(md)

generateReadme();

