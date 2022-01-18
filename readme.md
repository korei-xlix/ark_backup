# ARK バックアップ
**～取扱説明書 兼 設計仕様書～**

# システム概要 <a name="aSystemSummary"></a>
Windows環境化でARK:Survival Evolvedのローカルプレイにおけるセーブ領域のバックアップをおこないます。
なおPythonで動作します。インストール方法はこのreadmeに記載しています。
　　[ARK:Survival Evolved(steam)](https://store.steampowered.com/app/346110/ARK_Survival_Evolved/)

実験してないので確証ないですが、Pythonで動作するのでPythonがインストールされているサーバでも動作する可能性はあります。




# 目次 <a name="aMokuji"></a>
* [システム概要](#aSystemSummary)
* [前提](#aPremise)
* [デフォルトエンコードの確認](#aDefEncode)
* [セットアップ手順](#aSetup)
* [アップデート手順](#aUpdate)
* [起動方法](#aStart)
* [各機能](#aFunction)
* [本リポジトリの規約](#aRules)
* [参考記事](#aReference)




# 前提 <a name="aPremise"></a>
* python3（v3.8.5で確認）
* Windows 10
* githubアカウント
* デフォルトエンコード：utf-8




# デフォルトエンコードの確認　★初回のみ <a name="aDefEncode"></a>
本ソフトはデフォルトエンコード**utf-8**で動作することを前提に設計してます。
utf-8以外のエンコードでは誤動作を起こす場合があります。
pythonのデフォルトエンコードを確認したり、utf-8に設定する方法を示します。

```
# python
>>> import sys
>>> sys.getdefaultencoding()
'utf-8'
  utf-8が表示されればOKです。

>> exit
  ここでCtrl+Z を入力してリターンで終了します。
```

もしutf-8でなければWindowsの環境変数に PYTHONUTF8=1 を追加します。
「スタート」→「システムの詳細設定 で検索」→「詳細設定」→「環境変数」
ここに **変数名=PYTHONUTF8、変数値=1** を追加する。
設定したら上記エンコードの確認を再実行して確認しましょう。




# セットアップ手順 <a name="aSetup"></a>

1.pythonと必要なライブラリをインストールします。

インストーラを以下から取得します。基本的に * web-based installer を使います。
入手したインストーラで好きな場所にセットアップします。
  [python HP](https://www.python.org/)

Add Python x.x to Path はチェックしたほうがいいです。
その他はデフォルトか、環境にあわせてオプションを選択しましょう。
インストールが終わったらテストしてみます。

```
# python -V
Python 3.8.5
  ※Windowsの場合、python3ではなく、pythonらしいです

# pip3 list
～以下省略～
```

2.botソースの管理アプリとしてWindows版のgithubデスクトップを使います。

2-1.githubデスクトップをインストールします。
　　[githubデスクトップ](https://desktop.github.com)

2-2.githubの自分のアカウントに本家リポジトリをFork（コピー）する。
　　[ark_backupリポジトリ](https://github.com/korei-xlix/ark_backup)
  の右上あたりの[Fork]ボタンを押してください。
  すると、自分のアカウントに[自垢名 / lucibot_win]というリポジトリができます。

2-3.githubデスクトップで1項でForkしたリポジトリから自PCにクローンをダウンロードします。
  githubデスクトップのCurrent repository→Add→Cloneを選択します。
  任意のフォルダを選択してCloneを押してください。

2-4.自分のブランチを作ります。
  githubデスクトップのCurrent branch→New branchで任意の名前を入力します。




# アップデート手順 <a name="aUpdate"></a>
当方リポジトリのmasterから最新版をpullする方法です。  

1.githubデスクトップを起動します。

2.自分のark_backupリポジトリを選択し、Current branchをクリックします。

3.New branchをクリックし、バックアップ用のブランチを作成します。
  名前はわかりやすいように。

4.ブランチを[main]に切り替えます。

5.[Fetch Origin]をクリックします。

6.[Puch]をクリックします。

ここまでで、自分のリポジトリの[main]と、自PCのソースに最新が反映されてます。

もし不具合があったら...？
3項で保存したブランチに切り替えると、自PC側にアップデート前のソースが戻ってきます。
以後、アップデートがあったら[main]に切り替えて[Fetch]すれば、修正後のソースが反映されます。




# 起動方法 <a name="aStart"></a>
まずSteamクライアントのインストールフォルダを確認してください。
デフォルトだと以下のフォルダにインストールされてるはずです。
  C:/Program Files/Steam (x86)/

もし違っていたら、script/gval.pyの22行目を書き換えてください。


DOSのコマンドラインにて以下を入力します。

```
# cd [Lucibotのインストールフォルダ]
# python run.py
```

起動すると、コンソール画面が起動します。



# 各機能 <a name="aFunction"></a>
各機能を以下に説明します。
コマンドを実行するには、画面のプロンプトに指定のコマンドを入力します。
コマンドは全て\マークの後、半角英字を入力します。


<a id="iFunc_GetInfo"></a>
#### 手動バックアップ【 \mb 】
コマンド実行のタイミングでsavedフォルダをバックアップします。


<a id="iFunc_GetInfo"></a>
#### 定期バックアップ【 \cb 】
一定時間ごとにsavedフォルダをチェックし、データに更新があればバックアップします。
バックアップは、ARK側からコンソールコマンド SaveWorld を実施するか、ARKが定期セーブをおこなったタイミングでおこなわれます。
バックアップアーカイブは世代ごとに管理され、一定回数分は保持されます。




# 本リポジトリの規約 <a name="aRules"></a>
* 素材の改造、流用、配布について。  
  * このリポジトリ配下のソースの改造、改造物の配布は自由にやってください。  
    その際の著作権は放棄しません。  
  * 未改造物の再配布、クローンしたあと未改造のまま放置することは禁止とします。  
* 著作権について。
  * 著作権は放棄しません。
  * 別に著作権表記のある素材の利用については、各自で許諾を取得ください。  
    当方では責任を負いません。  
* 免責事項について。
  * 当ソースを使用したことによる不具合、損害について当方は責任を持ちません。  
    全て自己責任でお願いします。  
  * Web上やSNS上、オンライン上で発生した、わたしが関知していないトラブル、損害については、一切責任を負いません。  
    各自でご対応をお願いします。  
* 当ソースの仕様、不具合についての質問は受け付けません。自己解析、自己対応でお願いします。  
* このリポジトリに含まれるファイル構成を変えたり、消したりしないでください。誤動作の原因となります。  
* その他、ご意見、ご要望については、開発者ホームページを参照ください。  




# 参考記事 <a name="aReference"></a>
**※敬称略**  
* [Windows 上の Python で UTF-8 をデフォルトにする（methane）](https://qiita.com/methane/items/9a19ddf615089b071e71)




***
::Project= My Blog  
::Admin= Korei (@korei-xlix)  
::github= https://github.com/korei-xlix/  
::Homepage= https://koreixlix.wixsite.com/profile  
