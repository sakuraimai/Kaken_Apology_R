# Kaken_Apology_R
 
謝罪語を聞くことによる知覚実験プログラム。

ディレクトリ構造は以下
```
.
├── experiment_folder
│   ├── shuffled_wavfile: 実験時に実際にwavファイルが再生された順番を保持したファイルフォルダ
│   ├── wavfile: preproc.pyで作成したwavファイルの名前を列挙したファイルフォルダ
│   ├── condition.csv: preproc実行時に条件を指定するファイル
│   └── overview.csv: 設定した条件を保存するファイル
├── questionaires
│   └── example_question.csv: 実験画面の設問を編集するファイル
├── results
│   ├── data
│   │   └── data_kaken_apology: 前実験の結果全体を記述したファイル
│   ├── wav: 音声ファイルの置き場所 (.gitignore追加済)
│   ├── apology_test_r: 今回の実験(R)の結果を記述するファイル (.gitignore追加済)
│   ├── apology_test: 前回の実験の結果を記述したファイル
│   └── personal_info.csv
├── templates: 画面テンプレート(html)の置き場所
├── app.py: プログラム実行ファイル
└── preproc.py: wavファイルの名前を列挙するためのファイル
```

# Requirement
 
動かすのに必要なライブラリなどを列挙する
 
* python 3
* flask
* Mac with intel processor
 
# Installation
 
"Module not found"のエラーが出た場合、下記を試す
 
```bash
pip install モジュール名
```

# Usage

基本的にはプログラムファイル(.py)がある場所に移動して実行する。
(2022.6.2) preproc.pyの場所を変更。Kaken_Apology_Rの直下(app.pyと同じ場所)に移動。

## Preprocess



# Note
 
注意点などがあれば書く
 
