import os
import cv2 as cv
import json
from PIL import Image 
from PIL.ExifTags import TAGS
from tqdm import tqdm

fullDir = './fulls'
thumbDir = './thumbs'
metadataDir ='./metadata'
for createDir in [fullDir, thumbDir, metadataDir]: 
    if(not(os.path.exists(createDir))): os.mkdir(createDir)
imgNameJS = './imgNames.js'
imgNames = [imgName.split('.jpg')[0] for imgName in os.listdir(fullDir) if imgName.endswith('.jpg')]
newline = '\n'
empty = '' 

def makeTSList(split=2):
    with open(imgNameJS,'w') as file:
        arrayStr = 'const imgNames = ['
        for i,name in tqdm(enumerate(imgNames)): 
            arrayStr += f"\'{name}\'{'' if i == len(imgNames) - 1 else f',{newline if i % split == split-1 else empty}'}"
        arrayStr += '];'
        file.write(arrayStr)

def getThumbs(check=False):
    for name in tqdm(imgNames):
        thumbPath = f'./{thumbDir}/{name}.jpg'
        fullPath = f'{fullDir}/{name}.jpg'
        if(not(check) or not(os.path.exists(thumbPath))):
            img = cv.imread(fullPath)
            resized = cv.resize(img,(400,300))
            cv.imwrite(thumbPath,resized)

def getMetadatas(check=False):
    for name in tqdm(imgNames):
        fullPath = f'{fullDir}/{name}.jpg'
        metadataPath = f'{metadataDir}/{name}.json'
        if(not(check) or not(os.path.exists(metadataPath))):
            img = Image.open(fullPath)
            exifdata = img.getexif()
            metadata = {}
            for tagid , value in exifdata.items():
                tagname = TAGS.get(tagid,tagid)
                metadata[tagname] = value
            print(metadata)
            with open(metadataPath,'w') as metadataFile:
                json.dump(metadata,metadataFile)

if __name__ == '__main__':
    print('Making Timestamp List!');
    makeTSList()
    print('Making Thumbnails!')
    getThumbs()
    print('Extracting Metadata!')
    getMetadatas()