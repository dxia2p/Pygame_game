import json
import os

def SaveTilemap(tilemap, path = "TilemapFiles/tilemap.json"):

    #if not os.path.exists(path):
    tilemapFile = open("tilemap.json", "w")

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
                jsonObject = json.dumps(tileDict, 4)