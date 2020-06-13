
from PIL import Image
#import os
import glob
import numpy as np
from sklern.model_selection import train_test_split

#분류대상 카데고리 선택
caltech_dir = "C:\\Users\1l11l\OneDrive\바탕 화면\101_ObjectCategories"
categories = ["chair","camera","butterfly","elephant","flamingo"]
nb_classes = len(categories)

image_w = 64
image_h = 64
pixels = image_w * image_h *3

#이미지데이터 로드
X = []
Y = []
for idx, cat in enumerate(categories):
    label=[0 for i in range(nb_classes)]
    label[idx]=1
    #이미지
    image_dir = caltech_dir + "/"+cat
    files = glob.glob(image_dir+"/*.jpg")
    for i, f in enumerate(files):
    #for i, g in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        data = np.asarray(img)
        
        X.append(data)
        Y.append(label)
        if i%10 ==0:
            print(i, "\n",data)
          
                
X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = \
    train_test_split(X,Y)
xy  = (X_train, X_test, y_train, y_test)
np.save("./image/5obj.npy",xy)

print("ok",len(Y))