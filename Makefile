all:*.py
	del /Q dist
	pip install pyperclip
	pip install pyinstaller
	pyinstaller aqua.py --onefile --noconsole --icon=author.ico --exclude-module _bootlocale
	echo D | xcopy /Y /Q res dist\res /s
	del /Q build\aqua\*
	python archive.py