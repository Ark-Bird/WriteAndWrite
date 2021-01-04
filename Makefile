all:*.py
	del /Q dist
	pip install pyperclip
	pip install pyinstaller
	pyinstaller aqua.spec aqua.py --onefile --noconsole --icon=author.ico
	del /Q build\aqua\*