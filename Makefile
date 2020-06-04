all:*.py
	del /Q dist
	pyinstaller aqua.py --onefile --noconsole --icon=author.ico