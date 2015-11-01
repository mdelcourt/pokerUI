# Poker library
This repository contains two programs developed to manage poker tournaments, especially kotangente's poker.

PokerUI is a user interface to manage tables during the tournament while blindes displays informations and sponsors.

## Poker UI
### Overview
PokerUI is a tk interface built for the pokerlib library developed for smaller tournaments.
### Installation
From a standard linux distribution, the only extra packet needed is python-tk. For a debian based distribution, it will be installed by the "auto_install.sh" script used to build the "blindes" program.

Then, just run pokerUI.py.

### Features

Upon launching pokerUI, the main user interface opens. To start a tournament, you first have to load either a player list file or a save file. 

The "start default tournament" button will open the data/liste.txt file, and create a new tournament from it. Players will be randomly assigned to tables according to the settings in the configuration file. The format of the list file has to be the following : a unique player id, a tabulation, and the player name for each line. This corresponds to a copy-paste from a libreoffice spreadsheet (an example is available in the data folder).

To load another list of players or a save file from a previous tournament, go to file>open... enter the desired name and press "ok".

Once a tournament is created/loaded, the different tables created are displayed on the main screen. Under the table, comments and player operations are displayed.

Once a player is eliminated, click on the corresponding table and on "remove" next to the player's name. The player will disappear and the tables will be equilibrated. The operations done are displayed in the main window.

If, for some reason, a player has to be moved from a table to another, click on his table, then the button furthest to the right next to his name and select the desired destination table. Then, click on "Move to table".

If a player wasn't in the list and has to be manually added, select the desired table, then "Add player".

To save the state of a tournament or a list of its players, either click on "Save to file" for the default autosave.sav, or file>save...


### Configuration

The tournament configuration is described in config.py The most important parameters are the following:

* MAX_DIFF_gt_6 = 1

This option gives the maximum player difference allowed between tables in the tournament while the average number of players is greater than six. By default, it is set to 1 to have a tournament as fair as possible. This value can be changed to two to reduce the number of players being moved (it will decrease the average number of moves by 0.07 and the maximum number of moves a player has to do by 0.18 on standard options). 

* MIN_MOVE = True

When a table has to lose a player, choose from the players that moves the least.

* GLOBAL_MIN_MOVE = True

When a player has to be moved, select from the players of the whole tournament that moved the least.

* SOFT_GLMM_SEL = True

If GLOBAL_MIN_MOVE is selected, only choose from longest tables. False is not recommended.

* MIN_MOVE_ON_DEL = False

When deleting a table, chooses table with lowest number of total moves
* MIN_MAX_ON_DEL = True

When deleting a table, chooses from table in which the player that moved the most has the lowest moves. The two previous options obviously can't be true at the same time.
* SOFT_SEL_ON_DEL = False

When a table has to be deleted, only choose from smallest tables.

## Blindes
### Overview
The blindes program aims to display on screen informations relative to the status of the tournament. The current blind level, the time left, number of players, average stack and, if needed, the logo of sponsors.

### Installation
For a distribution from the debian family, the script auto_install.sh should successfully install the software.

If not, the following dependencies have to be installed
* SDL

This software uses the following sdl libraries :libsdl-ttf2.0-dev libsdl1.2-dev libsdl-image1.2-dev
* G++
* Vlc is used to play sounds, but is not required to run the main program

The program will then have to be compiled using the following command (written in compile.sh).

> g++ main.cpp `sdl-config --libs --cflags ` -lSDL_ttf -lSDL_image -o blindes.out

Then, the permissions have to be changed on the launcher in order to execute it.

### Features
Once the program is launched, it will read out information from the configuration files and start a new tournament (see next section). The first blind level will be selected and the timer will be paused. From there, the following actions are possible:
* Space bar : pause/unpause the timer
* + and - : change the number of players in the tournament
* t : Start the clock (60s to take a decision)
* press twice the arrow to the right/left : change blind level

### Configuration
#### blindes.txt
The blindes.txt file saves the different blind levels with the following format :
>SB-X BB-X A-X T-X

where X is the values (int) of the small blind, big blind, ante and time (in minutes) of the level. Then, at the end of the blind table :

>END

#### blindes.conf

* RES_X, RES_Y : Size of the window
* FONT, FONT_INFO, INTERLINE : size of the font and font for the tournament status. Padding size between lines.
* IMAGE : source of the picture to show. sponsor.jpg will be automatically changing through every .jpg picture in sponsor_folder.
* IMG_WIDTH : not (yet?) used
* SHORT_PAUSE : pause (in ms) after refreshing screen
* N_PLAYER : Starting number of players in tournament
* CHIPS_INIT : Starting number of chips per person

