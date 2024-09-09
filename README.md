# yogo_python

此專案為工研院瑜珈計畫中，python 研究的內容。


## 專案架構
- data: 資料集
- developer: 開發者研究用，不會放入 Android Studio 專案的檔案
- JsonFile: 瑜珈正確關節點的角度資訊
- root 資料夾的 py 檔
  - 為需要移植到 Android Studio 的檔案

### root 資料夾的 py 檔
- 關節點與角度
  - AngleNodeDef: 不同動作關心的關節點
  - AngleRegion
  - AngleCalculator: 輸入 Mediapipe 偵測結果，計算關節的角度
- 瑜珈教練系統
  - toolkit : 瑜珈教練系統的工具
  - yogaPoseDetect : 偵測瑜珈動作
- 分數計算
  - ScoreCalculator : 計算瑜珈教練系統的分數
- 瑜珈墊與腳定位
  - YogaMatProcessor : 負責將人體骨架的腳座標點，轉換成瑜珈墊上面的點
  - YogaMatRangeGetter : 偵測場景中的瑜珈墊座標
  - heatmap : 瑜珈墊與的 heatmap 圖
  - FeetData : 腳座標的資料
- 其他
  - yogaFileGetter : 取得每個動作所需的相關資料
  - config : 一些設定參數



## SetUp

```
pip install requirements.txt
```


## 新增新動作的流程

### 1. 資料集蒐集

`用途: 主要是以圖片配合 MideaPipe 偵測瑜珈動作的角度 json 檔，供分數計算器、教練系統使用`

- 可以去實驗室的Nas， `yoga project/DataSet` 中下載現有的資料集
- 資料集架構
  - Clean: 整理好的資料
    - first input: 所有整理好的資料
    - second input: 排除掉 MediaPipe 偵測不好的資料
  - Raw: 原始資料集
    - [Yoga Pose Image classification dataset](https://www.kaggle.com/datasets/shrutisaxena/yoga-pose-image-classification-dataset): 包含大量種類的瑜珈動作。命名是用梵文命名，請自行去 GPT 將所需瑜珈動作的英文翻譯成梵文
- 請將資料集整理到 first input 中，並為該瑜珈動作開一個資料夾
- 請將 [config.py](config.py) 的 dataset_path 設為資料集路徑


### 2. 新增基礎資料

- 在 [AngleNodeDef.py](AngleNodeDef.py) 新增該動作需要的關節點
- 在 [AngleRegion.py](AngleRegion.py) 新增該動作的 XXX
- 在 [yogaFileGetter.py](yogaFileGetter.py) 的 yogaFileDict 中，新增該動作的相關檔案


### 2. 瑜珈角度 json 檔製作

用途 : 詳情可[參考](JsonFile/README.md)
- 工作區: [angle_json_generator.py](developer/angle_jsonFile_creator.ipynb)
- 結束後，會在 JsonFile 資料夾中，產生以下 json 檔案:
  - 瑜珈教練系統用
    - JsonFile/pose/sample.json
  - 瑜珈評分系統用
    - JsonFile/pose/sample_score.json: 給予分數計算系統使用，平均關節點角度
    - JsonFile/pose/std_angle.json:  關節點角度標準差
    - JsonFile/pose/weight.json: 關節點的計分權重

### 3. 新增動作規則

在 [toolkit.py ](toolkit.py ) 中，新增動作的規則



### 4. 將檔案移動到 Android Studio 專案

請將 
- JsonFile
- 在本專案 root 資料夾底下所有的 .py 檔案，複製到 YogaAndroid 中的 app/src/main/python








