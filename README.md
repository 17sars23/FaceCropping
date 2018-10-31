# FaceCropping
複数枚の写真から自動で顔を検出し，好きな形に一括で切り抜く

## 環境
- Python3
- OpenCV

### Install
OpenCVのインストールには数分かかるかと...
``` brew install opencv ```

## Quick Start
1. `./pic/`に写真を格納．サブディレクトリありでもOK．
2. `$ python3 cropping.py` で実行．
`/result`に切り抜かれた正方形画像が保存され，`/check`に検出結果と切り抜き範囲が描画された画像が保存される．

### 切り抜きオプション
デフォルトは正方形に切り抜かれてます．
`/mask`の中に`1.png`の丸と`2.png`の11角形を用意してあり，
``` $ python3 cropping.py 1```
で実行すると丸く切り抜かれた透過画像が`mask_result_1`に保存されます．

``` $ python3 cropping.py <mask画像の名前(拡張子抜き)>```
で用意したお好みのマスク画像に切り抜きもできます．

## Usage
