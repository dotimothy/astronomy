import os
import cv2 as cv
from tqdm import tqdm

fullDir = './fulls'
thumbDir = './thumbs'
metadataDir ='./metadata'
imgNameJS = './imgNames.js'
imgTS = [imgName.split('.jpg')[0] for imgName in os.listdir(fullDir) if imgName.endswith('.jpg')]
newline = '\n'
empty = '' 

def makeTSList(split=2):
    with open(imgNameJS,'w') as file:
        arrayStr = 'const imgNames = ['
        for i,ts in tqdm(enumerate(imgTS)): 
            arrayStr += f"\'{ts}\'{'' if i == len(imgTS) - 1 else f',{newline if i % split == split-1 else empty}'}"
        arrayStr += '];'
        file.write(arrayStr)

def getThumbs(check=False):
    for ts in tqdm(imgTS):
        thumbPath = f'./{thumbDir}/{ts}.jpg'
        fullPath = f'{fullDir}/{ts}.jpg'
        if(not(check) or not(os.path.exists(thumbPath))):
            img = cv.imread(fullPath)
            resized = cv.resize(img,(400,300))
            cv.imwrite(thumbPath,resized)

def getMetadatas(check=False):
    for ts in tqdm(imgTS):
        fullPath = f'{fullDir}/{ts}.jpg'
        metadataPath = f'{metadataDir}/{ts}.json'
        if(not(check) or not(os.path.exists(metadataPath))):
            pass

if __name__ == '__main__':
    print('Making Timestamp List!');
    makeTSList()
    print('Making Thumbnails!')
    getThumbs()
    print('Extracting Metadata!')
    getMetadatas()