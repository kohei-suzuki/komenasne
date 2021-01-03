# komenasne について

### [ダウンロードはこちら](https://github.com/nyumen/komenasne/releases)

## 概要
nasneの動画再生と合わせて、ニコ生のタイムシフトの実況コメントを再生します。

同じネットワーク上のnasneの動画を再生した状態でこのスクリプトを起動することにより、  
コメント再生ソフトーのcommenomiやブラウザーで同チャンネル同時刻のニコ生実況タイムシフトが再生されます。  
Windows環境以外にMac環境でも起動します※後述  
  
  
## 説明
- nasneの再生に連動して、commenomi（こめのみ）もしくはニコ生を同期させるアプリです。
- Windows / Mac両対応、ただしプログラム言語「Python」の実行環境が必要です。
- 動作設定はiniファイル。事前に自分の環境に合わせてテキストエディタで書き換える必要あり（nasneのローカルIPやチャンネル設定など）
- nasneの再生環境は問いません、PS4 / スマホ / PC TV Plusどれでも可。
- 視聴したい録画番組を再生してまず一時停止、次にkomenasne.batを実行（Windowsの場合）。実況画面が開いたらフルスクリーンにしてnasneの再生を再開。するとnasneの再生に連動して実況が同期します。
- 関東・中部・関西のチャンネルに対応しています（プログラムが理解できる人は自分でチャンネルを登録することも可能です※後述）
- 直近30分以内のコメントは取得できません。


## 更新履歴
### 2021-01-03
- タイトルに[解]などが入った番組への対応
- デフォルトのコメント再生ソフトをcommeonからcommenomiに変更
- AT-Xチャンネルへの対応
- 四国エリアの放送局を追加
### 2020-12-31
- 実況ログの取得先をニコ生のタイムシフトからTVRemotePlus様の過去ログAPIに変更（ニコニコアカウントが不要になりました。過去すべての期間の動画に対応）
- コメント再生ソフトをjkcommentviewerからcommeonに変更
### 2020-12-30
- 中部、関西在住の方でもでも使用できるようにキー局と紐づけ
- 再生中の動画が見つからないときのメッセージ表示
- Windowsのセットアップをbatファイル化（pipモジュールをインストール）
- Windowsの起動をbatファイル化
- iniファイルのnasneの設定をカンマ区切りに変更
### 2020-12-28
- リリース


## 動作環境
コメント再生ソフトのcommenomiのダウンロードが必要です。 → commenomi (こめのみ) http://air.fem.jp/commenomi/
動画再生はPS4+torneでもスマホ+torneでもWindows機でPC TV Plusでも構いません。  
iniの設定により、commenomiの代わりにブラウザでニコ生のタイムシフトから表示することもできます※。    
Macでもブラウザからニコ生のタイムシフトで表示することが出来ます※。  
※プレミアムアカウント必須、公式チャンネルの3週間以内の動画まで。  


## セットアップ
Python3.x系のインストールが必要です。  
  
※Windowsの場合、Microsoft Storeで最新版を入れておくのが構築が楽かもしれません。  
https://www.microsoft.com/ja-jp/search?q=python  
  
Pythonインストール後に、setup.batを実行してください。
  
その後、komenasne.iniを開き、[NASNE]セクションの"ip"にカンマ区切りでIPを記入してください。  
nasneのIPはtorneの設定画面で確認できます。  
  
次に、commenomi_pathを自分の環境に修正してください。commenomi.exeのプロパティからパスをコピーできます。  
  
実況ログの保存先がデフォルトでtempディレクトリになっているため、ログを保存したい場合は kakolog_dir を変更してください。  

  
## 実行
torne等で動画を再生した直後に一旦停止してから、komenasne.batをダブルクリックで実行してください。  
その後、コメント再生画面を全画面にするなどしてから、動画の一旦停止を解除してから続きを再生してください。  
    
### commenomiの便利なショートカット
- SPACE 一時停止/再生
- A 最初のAのコメントに移動
- B 最初のBのコメントに移動
- C 最初のCのコメントに移動
- 0 先頭に戻る
- Ctrl + F コメント検索
- → 早送り
- ← 早戻し
- Ctrl + → 高速早送り
- Ctrl + ← 高速早戻し
- マウスのホイールで微調整

同じネットワーク上であればいいので、PS4でテレビに動画を再生しながらPCのコメントをチラ見する、といった事が可能です。  
「PC TV Plus」と「commenomi」の組み合わせであれば、ニコ生のようにコメントをオーバーレイ表示することも可能です。  
Windows機の場合、ALTキーを押しながらTABでタスクを切り替えるのが使いやすいです。  
  
  
## Macでの動作
Python公式サイトから最新版をインストールしてください。  
次にコマンドラインで以下を実行してください。  
pip install requests  
pip install beautifulsoup4  

ターミナルで"python3 komenasne.py" と入力することでブラウザでニコ生のタイムシフトが開きます。  
  
  
## 関東・中部・関西以外のチャンネル追加
channellist.py を開き、nasne_ipを自分のnasneに書き換えてから実行した出力結果をもとに、komenasne.pyを修正してください。  


## スペシャルサンクス
- commenomi (こめのみ) http://air.fem.jp/commenomi/
- ニコニコ実況 過去ログ API https://jikkyo.tsukumijima.net/
