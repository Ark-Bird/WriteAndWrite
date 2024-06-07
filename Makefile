delyv:
	cp wanabi\\*.py ..\..\onedrive\Light-author\wanabi
all:
	deactivate
	git checkout master
	del /Q dist
	pyinstaller aqua.py --noconsole --onefile --icon=author.ico --exclude-module _bootlocale
	echo D | xcopy /Y /Q res dist\res /s
	del /Q build\aqua\*
	python archive.py
	git checkout develop
	activate
stable:
	git checkout stable
	git push
	git checkout develop
deploy:
	git checkout master
	git merge stable
	git push
	git checkout develop
pull:
	git pull
	git checkout stable
	git pull
	git checkout master
	git pull
	git checkout develop
dev:
	git checkout develop
merge:
	git checkout stable
	git merge develop
	git checkout develop
base:
	git checkout develop
	git push