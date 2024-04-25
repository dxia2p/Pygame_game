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

    outputList.append({"IsCompressed": False})

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

 # I will use BFS to split the tilemap up into rectangles. This may not yield the minimum number of rectangles in some cases, but the solution to get the minimum is too complicated and slow.
def SaveTilemapCompressed(tilemap, path="TileFiles/tilemap.json"):
    visited = [[False] * len(tilemap[i]) for i in range(len(tilemap))]

    tilemapFile = open(path, "w")
    outputList = []

    outputList.append({"IsCompressed": True})

    for i in range(len(tilemap)):
        for j in range(len(tilemap)):
            if not visited[i][j] and tilemap[i][j] != None:
                targetId = tilemap[i][j].tileTemplate.id
                startTile = [i, j]
                targetTile = [i, j] # first move x right until not possible, then move y down until not possible
                while tilemap[targetTile[0] + 1][targetTile[1]] != None and tilemap[targetTile[0] + 1][targetTile[1]].tileTemplate.id == targetId and (not visited[targetTile[0] + 1][targetTile[1]]):
                    visited[targetTile[0] + 1][targetTile[1]] = True
                    targetTile[0] += 1
                print(f"Target tile: {targetTile}, Start Tile: {startTile}")
                # now expand down
                canProceed = True
                while canProceed:
                    canProceed = True
                    for k in range(startTile[0], targetTile[0] + 1):
                        if tilemap[k][targetTile[1] + 1] == None or tilemap[k][targetTile[1] + 1].tileTemplate.id != targetId or visited[k][targetTile[1] + 1]:
                            canProceed = False

                    if canProceed:
                        targetTile[1] += 1
                        for k in range(startTile[0], targetTile[0] + 1):
                            visited[k][targetTile[1]] = True

                rectDict = {
                    "StartPosition": [startTile[0], startTile[1]],
                    "EndPosition": [targetTile[0], targetTile[1]],
                    "Id": targetId
                }

                outputList.append(rectDict)

    jsonObject = json.dumps(outputList, indent=2)
    try:
        tilemapFile.write(jsonObject)
    except:
        print("Error occured during saving tiles")
    print("Finished saving tilemap")
    tilemapFile.close()
                
                

def LoadTileTemplates(path = "TileFiles/tileTemplates.json"):
    tileTemplatesFile = open(path, "r")
    parsedJsonData = json.loads(tileTemplatesFile.read())
    tileTemplatesFile.close()
    return parsedJsonData

def LoadTilemap(path = "TileFiles/tilemap.json"): # Data is parsed in LevelEditor.py
    tilemapFile = open(path, "r")
    parsedJsonData = json.loads(tilemapFile.read())
    tilemapFile.close()
    return parsedJsonData

def LoadTilemapCompressed(path = "TileFiles/tilemap.json"): # Data is parsed in LevelEditor.py
    tilemapFile = open(path, "r")

    pass