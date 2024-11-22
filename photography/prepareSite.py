import os
import cv2 as cv
import json
from tqdm import tqdm
import exifread

fullDir = './fulls'
thumbDir = './thumbs'
metadataDir ='./metadata'
for createDir in [fullDir, thumbDir, metadataDir]: 
    if(not(os.path.exists(createDir))): os.mkdir(createDir)
imgNameJS = './imgNames.js'
imgNames = [imgName.split('.jpg')[0] for imgName in os.listdir(fullDir) if imgName.endswith('.jpg')]
imgNames.sort()
newline = '\n'
empty = '' 

def makeTSList(split=2):
    with open(imgNameJS,'w') as file:
        arrayStr = 'const imgNames = ['
        for i,name in tqdm(enumerate(imgNames)): 
            arrayStr += f"\'{name}\'{'' if i == len(imgNames) - 1 else f',{newline if i % split == split-1 else empty}'}"
        arrayStr += '];'
        file.write(arrayStr)

def getThumbs(check=False,size=(400,300)):
    for name in tqdm(imgNames):
        thumbPath = f'./{thumbDir}/{name}.jpg'
        fullPath = f'{fullDir}/{name}.jpg'
        if(not(check) or not(os.path.exists(thumbPath))):
            img = cv.imread(fullPath)
            resized = cv.resize(img,size)
            cv.imwrite(thumbPath,resized,[cv.IMWRITE_JPEG_QUALITY,80])

def getMetadatas(check=False):
    for name in tqdm(imgNames):
        fullPath = f'{fullDir}/{name}.jpg'
        metadataPath = f'{metadataDir}/{name}.json'
        if(not(check) or not(os.path.exists(metadataPath))):
            with open(fullPath,'rb') as full:
                tags = exifread.process_file(full)
                metadata = {} 
            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                    metadata[tag] = str(tags[tag])
            with open(metadataPath, 'w') as metadataFile:
                json.dump(metadata,metadataFile,indent=4)

if __name__ == '__main__':
    print('Making Timestamp List!');
    makeTSList()
    print('Making Thumbnails!')
    getThumbs(check=False)
    print('Extracting Metadata!')
    getMetadatas(check=False)