import json
import os

def SaveTileTemplates(tileTemplates, path = "TileFiles/tileTemplates.json"):
    tileTemplatesFile = open(path, "w")
    outputList = []

    for tileTemplate in tileTemplates:
        tileTemplateDict = {
            "Path": tileTemplate.texturePath,
            "Id": tileTemplate.id
        }
        outputList.append(tileTemplateDict)
    
    jsonObject = json.dumps(outputList, indent = 2)
    try:
        tileTemplatesFile.write(jsonObject)
    except:
        print("Error occured during saving tile templates")
    print("Finished saving tile templates")
    tileTemplatesFile.close()

def SaveTilemap(tilemap, path = "TileFiles/tilemap.json"):
    tilemapFile = open(path, "w")
    outputList = []

    for i in range(len(tilemap)):
        for j in range(len(tilemap[i])):
            if(tilemap[i][j] != None):
                tile = tilemap[i][j]
                pos = tile.position
                tileDict = {
                    "Position": [pos.x, pos.y],
                    "Id": tile.tileTemplate.id,
                }
                outputList.append(tileDict)

    jsonObject = json.dumps(outputList, indent=2)
    try:
        tilemapFile.write(jsonObject)
    except:
        print("Error occured during saving tiles")
    print("Finished saving tilemap")
    tilemapFile.close()

def SaveTilemapCompressed(tilemap, path = "TileFiles/tilemap.json"):
    pass

def LoadTileTemplates(path = "TileFiles/tileTemplates.json"):
    tileTemplatesFile = open(path, "r")
    parsedJsonData = json.loads(tileTemplatesFile.read())
    tileTemplatesFile.close()
    return parsedJsonData

def LoadTilemap(path = "TileFiles/tilemap.json"):
    tilemapFile = open(path, "r")
    parsedJsonData = json.loads(tilemapFile.read())
    tilemapFile.close()
    return parsedJsonData

def LoadTilemapCompressed(tilemap, path = "TileFiles/tilemap.json"):
    pass

