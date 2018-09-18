# Distance adventure IGT
Simple script that shows your current adventure mode run's IGT according to your save data after
each level is completed. This allows you to see the in-game time for your rub without having
to make a new profile every time. It also shows you more decimal places (3 compared to the
1 showed in the game).

## How to use
Short and sweet:  
    
    $ git clone https://github.com/TntMatthew/distance-advigt.git
    $ pip install distanceutils
    $ python advigt.py

When starting the script for the first time, it'll ask you for your log file and profile data.
It should be able to autodetect the location, but if it can't find them, it'll ask you to input
them manually. These will be saved in config.json.

Once the script is running, it'll show you your total and segment IGT once each map is completed. Note that since this is based on log-reading, the script might freak out a bit
if you open it while the log still has meaningful content in it, so I reccomend only
running the script once you've already started the game.