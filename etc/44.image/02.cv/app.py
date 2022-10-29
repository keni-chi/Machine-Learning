import cv2

# 分類器
cascadeFile = "C:/xxx/haarcascade_frontalface_default.xml"

# 分類器の設定
cascade = cv2.CascadeClassifier(cascadeFile)

# 入力ファイル
imageImput ="C:/xxx/001.jpg"

# 入力ファイルをリードする
image = cv2.imread(imageImput)

#グレースケールにする
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 出力ファイル
imageOutput = "C:/xxx/001outface.jpg"

# 顔を認識する
facerect = cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

# 顔を検出できた際の処理
if len(facerect) > 0:
    # 顔
    print(facerect)
    x = facerect[0][0]
    y = facerect[0][1]
    x_width = facerect[0][2]
    y_width = facerect[0][3]
    print(x, y, x_width, y_width)

    # 顔に枠を付ける
    for rect in facerect:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)

    # 結果を画像として保存する
    cv2.imwrite(imageOutput, image)

print('------------------------------------------------------')

# 分類器
cascadeFile = "C:/xxx/haarcascade_mcs_nose.xml"

# 分類器の設定
cascade = cv2.CascadeClassifier(cascadeFile)

# 入力ファイル
imageImput ="C:/xxx/001.jpg"

# 入力ファイルをリードする
image = cv2.imread(imageImput)

#グレースケールにする
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 出力ファイル
imageOutput = "C:/xxx/001outnose.jpg"

# 顔を認識する
facerect = cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

# 顔を検出できた際の処理
if len(facerect) > 0:
    # 顔
    print(facerect)
    x = facerect[0][0]
    y = facerect[0][1]
    x_width = facerect[0][2]
    y_width = facerect[0][3]
    print(x, y, x_width, y_width)

    # 顔に枠を付ける
    for rect in facerect:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)

    # 結果を画像として保存する
    cv2.imwrite(imageOutput, image)
