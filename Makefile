all:*.py
	del /Q dist
	pip install pyperclip
	pip install pyinstaller
	pyinstaller aqua.py --onefile --noconsole --icon=author.ico --exclude-module _bootlocale
	echo D | xcopy /Y /Q res dist\res /s
	del /Q build\aqua\*
	python archive.py
stable:
	git checkout stable
	git merge develop
	git push
	git checkout develop
deploy:
	git checkout master
	git merge stable
	git push
	git checkout develop