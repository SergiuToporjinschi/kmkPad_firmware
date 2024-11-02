import json

def readLayerDescriptor():
    with open('../../layersMap.json') as f:
        return json.load(f)
        


def getAllActiveLayerMaps():
    maps = readLayerDescriptor()
    # iterate through the layers and return the maps
    for layer in maps:
        print(layer)
        print(layer['Name'])
        print(layer['Active'])
        
    return maps
