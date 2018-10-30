# -*- coding:utf-8 -*-
import cv2
import sys
import os
import shutil
import glob


def FacePosition(image_path, Output_dir):
    #ファイル読み込み
    image = cv2.imread(image_path)
    if(image is None):
    	print(image,'Cannot open the image.')
    	quit()

    #グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #カスケード分類器の特徴量を取得する
    cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    #物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
    print(image_path,facerect)

    #顔の切り出し、複数候補がある場合最大面積を採用
    S = 0
    if len(facerect) > 0:
        for rect in facerect:
            width = rect[2]
            height = rect[3]
            if S <= (width * height):
                S = width * height
                x = rect[0]
                y = rect[1]
                max_width = rect[2]
                max_height = rect[3]

        dst = image[y:y+max_height, x:x+max_width]

        #出力ディレクトリの設定
        other, dir = os.path.split(os.path.dirname(i))
        tmp_dir = Output_dir + dir + "/"
        os.makedirs(tmp_dir, exist_ok=True)
        OutPath = tmp_dir + os.path.basename(i)

        cv2.imwrite(OutPath, dst)


if __name__=="__main__":

    #image_path = args[1]
    image_dir = "./pic/"

    #ディレクトリ内の検索＆画像のリスト化
    img = []
    for x in glob.glob(image_dir+'**/*.jpg', recursive=True):
        img.append(x)

    #出力ディレクトリ作成
    Output_dir = "./crop_pic/"
    os.makedirs(Output_dir, exist_ok=True)

    for i in img:
        FacePosition(i, Output_dir)
