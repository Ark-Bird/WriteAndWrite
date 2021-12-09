手っ取り早く使いたい人↓  
====
Windowsならdistフォルダにあるaqua.exeをダブルクリックで実行できます  
distフォルダをコピーすれば別の場所でも使うことができます。  
resについては要不要について考え中です
レジストリ等は使用しませんので必要な場所に置いてダブルクリックすれば起動します  
---
配布用にzipファイルを生成するように変更しましたmake一発で必要なファイルの入ったzipが生成されます  
展開したzip内のaqua.exeをダブルクリックで実行できます  
zipでできたresフォルダを削除しないでください、依存ファイルが入っています  
アンインストール時には削除して問題ありません  
  
====

Pythonをインストールできる方で詳細を追いたい方は以下になります。    
makeコマンドを実行してください  
makeコマンドはGNUの皆さんが作ってくれた物を使用します  
検索すればヒットするのでそれを使用してください  
Makeをインストールしたくない人は以下  
pip install pyperclip  
pip install pyinstaller  
pyinstaller aqua.py --onefile --noconsole --icon=author.ico --exclude-module _bootlocale  
ただしバイナリはやや重いのでpythonインタプリタで直接実行することを推奨します  
  
  
細かい実装を知りたい人  
----
aqua.pyに書いてあります、それ一つで全ての機能をまかなっています  
  
Notice!  
----
pyperclipに依存しているのでスクリプト単体で実行する場合はpip等で別途インストールしてください。  
当ソフトは現在64bitのWindows10環境でのみサポートしています  
※非推奨ではありますがこのバイナリをアンチウイルスソフトのホワイトリストに登録すると多少軽くなります  


-------------
LICENSE
====
当ソフトはMITライセンスで配布されます
----  
ver0.2.03


  
  
-----------------------------------
Al Sweigart al@inventwithpython.com  
BSD License  
↑pyperclipのライセンス表記