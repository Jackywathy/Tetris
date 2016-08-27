from cx_Freeze import setup,Executable

includefiles = ['1.txt','2.txt','3.txt','4.txt','5.txt','6.txt','7.txt','Comic.ttf','dog1.jpeg','Papyrus.ttc','boardre.py','Tetris.ogg']
includes = []
excludes = ['Tkinter']
packages = ['pygame']


setup(
    name = 'myapp',
    version = '0.1',
    description = 'A general enhancement utility',
    author = 'lenin',
    author_email = 'le...@null.com',
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('Game.py')]
)
