all:*.py
	deactivate
	del /Q dist
	pyinstaller aqua.py --onefile --icon=author.ico --exclude-module _bootlocale
	echo D | xcopy /Y /Q res dist\res /s
	del /Q build\aqua\*
	python archive.py
	activate
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