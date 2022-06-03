# Kaken_Apology_R
 
謝罪語を聞くことによる知覚実験プログラム

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
 
* python 3
* flask
* Mac with intel processor
 
# Installation
 
"Module not found"のエラーが出た場合、下記を試す
 
```bash
pip install モジュール名
```

# Usage

* 基本的にはプログラムファイル(.py)がある場所に移動して実行する

```bash
cd "directory_name" //"directory_name"に移動
cd .. //一つ上のdirectoryに移動
```

* (2022.6.2) preproc.pyの場所を変更。Kaken_Apology_Rの直下(app.pyと同じ場所)に移動。
* ターミナルで下記を実行して、/Desktop/Kaken_Apology_R が表示されたらOK
```
pwd
```

## Preprocess
### 条件設定
condition.csvを直接編集して条件を指定する
  * 1列: 話者正規表現で指定
  * 2~9列: それぞれの謝罪語に対して、含める場合(1)含めない場合(2)
  * 10列: 各被験者の各謝罪語を何語ずつ取得するか
  * 11列: 話者mixするかどうか
  * 12列: 謝罪語mixするかどうか
  * 13列: どの要素でまとまりを作るか

### 条件として設定できるもの
  - id①（謝罪語①→②→...）→id②（謝罪語①→…）
    - id_mix: 0, word_mix: 0, chunk: id(1)
  - id①（謝罪語mix）→id②（謝罪語mix）
    - id_mix: 0, word_mix: 1, chunk: id
  - 謝罪語①（id①→id②→…）→謝罪語②（id①→id②→…）
    - id_mix: 0, word_mix: 0, chunk: word(2)
  - 謝罪語①（id mix）→謝罪語②（id mix）
    - id_mix: 1, word_mix: 0, chunk: word
  - 完全ランダム
    - id_mix: 1, word_mix: 1, chunk: None(0)

```
含める話者(ファイル名のフォーマットを正規表現で指定),ごめんなさい,ごめんね,ごめん,すみません,すみませんでした,申し訳ありません,申し訳ありませんでした,申し訳ないです,何語ずつ含めるか,話者mix,謝罪語mix,chunk(0:None/1:id/2:word)
P2022031\w{7},1,1,1,0,0,0,0,0,40,0,0,1
```
### Run preproc.py

```
python preproc.py
```
## 実験プログラム
### 設問の編集

example.csvを編集することで、実験画面に表示する設問の表現を変えることができます

```
 questionaires
 └── example_question.csv
```

qの列を直接編集してください

```
Index,q
1,誠意を感じますか
2,certainty
3,謝られているように感じますか
4,certainty
```

### Run app.py

```
python app.py
```

