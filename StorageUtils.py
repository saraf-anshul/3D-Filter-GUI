import sys, os
import subprocess, shlex
import json
import shutil
from FilterUtils import *

def getLocationsFile():
	return os.path.join(os.path.expanduser('~'), "Documents/locations.json")

def getDefaultStorageLocation():
	return os.path.join(os.path.expanduser('~'), "Downloads/")

def zipDir( dirLocation : str, outputLocation : str ):
    shutil.make_archive(outputLocation, 'zip', dirLocation)
    print(f" files saved to {outputLocation}")


def createFilterFiles( filterName : str,\
    filterVersion : str,\
    filterImageDir : str,\
    outputLocation : str, \
    customResourceData : str = ""  ) -> str:
    # create new folder to zip
    # add index, sticker, png files
    os.system(f"mkdir {filterName}")
    os.system(f'cp "{filterImageDir}" {filterName}/{filterName}.png')
    os.system(f'echo "{getIndexFileData(filterName, filterVersion)}" > {filterName}/index.yaml')
    os.system(f'echo "{getShaderData(filterName + ".png")}" > {filterName}/facemask.mat')

    # test custom resource
    if( customResourceData != "" ):
        os.system(f'echo "{customResourceData}" > {filterName}/resource.json')
    else:
        os.system(f'echo "{getResourceFIle()}" > {filterName}/resource.json')

    return os.path.join(os.getcwd(), filterName)

def deleteFiles( location : str ):
    os.system(f"rm -rf {location}")


def transformAndSave( 
    filterName : str,\
    filterVersion : str,\
    filterImageDir : str,\
    outputLocation : str, \
    customResourceData : str = "" ):
    
    s = createFilterFiles( filterName, filterVersion, filterImageDir, outputLocation, customResourceData )
    zipDir( s, f"{outputLocation}/{filterName}" )
    deleteFiles( s )
    print(filterName, filterVersion, filterImageDir, outputLocation)

def mapToJsonString(map : dict) -> str : 
    return json.dumps(map).replace('"', '\\"') # for shell formatting

    