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
    	print(image_path,'Cannot open the image.')
    	quit()

    #切り抜きサイズの取得
    img_h, img_w = image.shape[:2]
    side = img_h if img_h < img_w else img_w

    #グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #カスケード分類器の特徴量を取得する
    cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    #物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=3, minSize=(100, 100))

    #顔の切り出し、複数候補がある場合最大面積を採用
    S = 0
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

        #検出した顔を囲む矩形の作成
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)
        cv2.rectangle(image, (startX, 0),(startX+side, side), (255, 255, 0), thickness=2)

        #認識結果の保存
        check = "./check/" + os.path.basename(i)
        cv2.imwrite(check, image)

        return OutPath
    else:
        print("Cannot find face:", image_path)


def Masking(squareImagePath, maskImagePath):
    #画像の読み込み
    img = cv2.imread(squareImagePath)
    if(img is None):
    	print(squareImagePath,'Cannot open the image.')
    	quit()
    #マスクをグレースケールで読み込む
    mask = cv2.imread(maskImagePath, 0)
    #BGRにチャンネル分解
    bgr = cv2.split(img)
    #画像のリサイズ
    img_h, img_w = img.shape[:2]
    mask = cv2.resize(mask, (img_h, img_w))
    bgra = cv2.bitwise_and(img, img, mask=mask)
    #透明チャンネル(マスク)を追加
    #bgra = cv2.merge(bgr + [mask])
    cv2.imwrite("new.png", bgra)


if __name__=="__main__":

    args = sys.argv
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
        squareImagePath = FacePosition(i, Output_dir)

        if len(args) == 2 and squareImagePath != None:
            key = args[1]
            maskImagePath = "./mask/" + key + ".png"

            Mask_dir = "./mask_result_" + key + "/"
            os.makedirs(Mask_dir, exist_ok=True)

            Masking(squareImagePath, maskImagePath)
