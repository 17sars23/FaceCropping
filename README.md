# FaceCropping
複数枚の写真から自動で顔を検出し一括で正方形に切り抜く

## 環境
- Python3
- OpenCV

インストール（完了するのに数分かかります．）
``` brew install opencv ```

## 実行
1, `./pic/`に写真を格納．サブディレクトリありでもOK．
2, `$ python3 cropping.py` で実行．`/result`に切り抜かれた画像が保存され，`/check`に検出結果と切り抜き範囲が描画された画像が保存される．
