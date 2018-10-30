# -*- coding:utf-8 -*-
import cv2
import sys
import os
import shutil
import glob
#from PIL import Image, ImageDraw


def FacePosition(image_path, Output_dir):

    #ファイル読み込み
    image = cv2.imread(image_path)
    if(image is None):
    	print(image,'Cannot open the image.')
    	quit()

    #切り抜きサイズの取得
    img_h, img_w = image.shape[:2]
    side = img_h if img_h < img_w else img_w
    #side = int(side*0.8)

    #グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #カスケード分類器の特徴量を取得する
    cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    #物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=3, minSize=(50, 50))
    #print(image_path,facerect)

    #顔の切り出し、複数候補がある場合最大面積を採用
    S = 10000
    if len(facerect) > 0:
        for rect in facerect:
            width, height = rect[:2]
            if S <= (width * height):
                S = width * height
                x, y, max_width, max_height = rect[:]
            else:
                continue

        startX = int(x+(max_width/2)-side/2)
        dst = image[0:side, startX:startX+side]

        #出力ディレクトリの設定
        other, dir = os.path.split(os.path.dirname(i))
        tmp_dir = Output_dir + dir + "/"
        os.makedirs(tmp_dir, exist_ok=True)
        OutPath = tmp_dir + os.path.basename(i)

        cv2.imwrite(OutPath, dst)
        #print("Success!", image_path)

        #検出した顔を囲む矩形の作成
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)
        cv2.rectangle(image, (startX, 0),(startX+side, side), (255, 255, 0), thickness=2)

        #認識結果の保存
        check = "./check/" + os.path.basename(i)
        cv2.imwrite(check, image)
    else:
        print("Cannot find face:", image_path)


if __name__=="__main__":

    #image_path = args[1]
    image_dir = "./pic/"

    #ディレクトリ内の検索＆画像のリスト化
    img = []
    for x in glob.glob(image_dir+'**/*.jpg', recursive=True):
        img.append(x)

    #出力&顔検出確認ディレクトリ作成
    Output_dir = "./result/"
    Check_dir = "./check/"
    os.makedirs(Output_dir, exist_ok=True)
    os.makedirs(Check_dir, exist_ok=True)

    for i in img:
        FacePosition(i, Output_dir)
