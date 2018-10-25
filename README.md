# Contributing

These are the libraries used

```
Flask
Flask-WTF (easy html form library)
PyQt5 (used for chromium web page)
Jinja2 (HTML Markup language)
```

### IDE
I suggest PyCharm, although any text editor works.

## Quick Start
Download python 3

Clone the repo

ensure python is installed (run `python --version`, you may need to run `python3 --version`)

run 
```
cd TGDKiosk
python -m venv venv
```

On windows run `venv\Scripts\activate.bat` in Command Prompt / Powershell

on Mac / Linux run `source venv/Scripts/activate`

whenever you want to run the app you must use the virtualenv with the above commands.

run `pip install -r requirements.txt`

now to run the app just type `python app.py` which should open the app window.


### Creating Game Configs

games are in `/TGDKiosk/static/game_configs/author_title/data.yaml` replacing author & title with the author and title of the game. 

Format like this

```
!Game
title: title
author: author
summary: summary
group: !Group TGD
banner: games/mygame/banner.png
path: games/mygame/gameexe.exe
disableReview: False
```

Game files (banner, exe) should go in `/TGDKiosk/static/games/author_title/` replacing author and title with the games author and title.
### PyCharm

Create a new venv for this project, install from requirements.txt (it should detect it automatically)

Build / run config you'll want just a regular python script targeting `app.py` 

For Flask (run in browser, easier for developing)
![](https://i.imgur.com/F49AHBh.png)

For Gulp (for editing semantic theme this is a must)
![](https://i.imgur.com/PMSEYxf.png)

For running the App (mostly testing stuff)
![](https://i.imgur.com/SXwysBS.png)
## If you want to modify LESS (Colors and stuff)
Download and install node.js.
### Windows
go to [nodejs](https://nodejs.org) and download / install the exe.

### Mac
for mac use [homebrew](https://brew.sh/)
open a terminal and run `brew install node`

### Linux
it depends on what distro you're running and if you're using linux I'm sure you can already figure it out.
[Some are here](https://semantic-ui.com/introduction/getting-started.html)

### After
run `npm install -g gulp`

open cmd / powershell / terminal and navigate to the TGDKiosk folder

run `npm rebuild`

All editing should be done in `semantic/src/site` See [Semantic-UI Theming](https://semantic-ui.com/usage/theming.html)

