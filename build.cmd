pip install -r requirements.txt
pyinstaller --onefile main.py
cd dist
del MarioPy.exe
rename main.exe MarioPy.exe
cd ..