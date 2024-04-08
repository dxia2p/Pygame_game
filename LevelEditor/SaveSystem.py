import json
import os

def SaveTilemap(tilemap, path = "TilemapFiles/tilemap.json"):
    #if not os.path.exists(path):
    tilemapFile = open("TilemapFiles/tilemap.json", "w")
    outputList = []

    for i in range(len(tilemap)):
        for j in range(len(tilemap[i])):
            if(tilemap[i][j] != None):
                tile = tilemap[i][j]
                pos = tile.position
                tileDict = {
                    "PositionX": pos.x,
                    "PositionY": pos.y,
                    "Id": tile.tileType.id,
                }
                outputList.append(tileDict)

    jsonObject = json.dumps(outputList, indent=2)
    try:
        tilemapFile.write(jsonObject)
    except:
        print("Error occured during saving tiles")
    tilemapFile.close()
    