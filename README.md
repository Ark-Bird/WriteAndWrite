手っ取り早く使いたい人↓  
====
makeコマンドを実行してください  
makeコマンドはGNUの皆さんが作ってくれた物を使用します  
検索すればヒットするのでそれを使用してください  
Makeをインストールしたくない人は以下  
pip install pyperclip  
pip install pyinstaller  
pyinstaller aqua.spec aqua.py --onefile --noconsole --icon=author.ico  
このコマンドでバイナリが生成されます  
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
ver0.1.12


  
  
-----------------------------------
Al Sweigart al@inventwithpython.com  
BSD License  
↑pyperclipのライセンス表記