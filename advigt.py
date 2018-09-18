import distance, os, sys, time, datetime, json

try:
    with open("config.json") as f:
        config = json.load(f)
except FileNotFoundError:
    print("Configuration file does not exist. Creating a config.json...")
    config = {}

try:
    log = open(config["log"])
except KeyError:
    if sys.platform == "win32":
        assumedlog = 'C:/Program Files (x86)/Steam/steamapps/common/Distance/Distance_Data/output_log.txt'
    elif sys.platform == "darwin": #macOS
        assumedlog = '~/Library/Logs/Unity/Player.log'
    elif sys.platform == "linux" or sys.platform == "linux2":
        assumedlog = '~/.config/unity3d/Refract/Distance/Player.log'
    if os.path.isfile(assumedlog):
        print(f"Log autodetected as {assumedlog}")
        config["log"] = assumedlog
        log = open(os.path.expanduser(assumedlog))
    else:
        print('Your logfile location could not be found.')
        config["log"] = input('Type the location of your game output log: ')
        log = open(config["log"])


if sys.platform == "win32":
    saveloc = '~/Documents/My Games/Distance/Profiles/Progress'
elif sys.platform == "darwin":
    saveloc = '~/Library/Application Support/Refract/Distance/Profiles/Progress'
elif sys.platform == "linux" or sys.platform == "linux2":
    saveloc = '~/.config/refract/Distance/Profiles/Progress'

try:
    profpath = os.path.expanduser(f'{saveloc}/{config["profile"]}')
except KeyError:
    profiles = os.listdir(os.path.expanduser(f'{saveloc}'))
    if len(profiles) < 2:
        profpath = os.path.expanduser(f'{saveloc}/{profiles[0]}')
        print(f'Profile filename auto-set to {profiles[0]}')
        config["profile"] = profiles[0]
    else:
        print(f'Multiple profiles detected.')
        index = 0
        for prof in profiles:
            print(f'{index}: {prof}')
            index += 1
        savename = profiles[int(input(f'Type the number of the correct profile: '))]
        profpath = os.path.expanduser(f'{saveloc}/{savename}')
        config["profile"] = savename
    
with open("config.json", "w") as f:
    json.dump(config, f)

progress = distance.ProfileProgress(profpath)

timeoffset = progress.stats.modes_offline[9]
curtime = 0

isfullrun = False
started = False

print('-- Current Time: 0')
print('-- Waiting for your glorious run to begin')

def pretty_time(s):
    return datetime.timedelta(seconds=round(s, 3))

print(f'-- Time offset: {pretty_time(timeoffset)}')

previousLevelName = ""

while True:
    where = log.tell()
    line = log.readline()
    if not line:
        time.sleep(0.1)
        log.seek(where)
    else:
        if line.startswith('>>> Loaded Scene: GameMode, Mode: Adventure'):
            print(f'[log] {line}')

            if started == True:
                progress = distance.ProfileProgress(profpath)
                segtime = (progress.stats.modes_offline[9] - timeoffset) - curtime
                curtime = (progress.stats.modes_offline[9] - timeoffset)
                print(f'{previousLevelName} | {pretty_time(segtime)} | {pretty_time(curtime)}')

            protolevelname = line[52:]
            previousLevelName = protolevelname[:protolevelname.index(',')]

            if 'Instantiation' in line:
                print('-- Started')
                started = True
            elif 'Credits' in line:
                print('-- Credits level loaded - marking as full run')
                isfullrun = True
        elif line.startswith('>>> Loaded Scene: MainMenu'):
            print(f'[log] {line}')
            if isfullrun:
                print(f'-- Run complete')
                progress = distance.ProfileProgress(profpath)
                segtime = (progress.stats.modes_offline[9] - timeoffset) - curtime
                curtime = (progress.stats.modes_offline[9] - timeoffset)
                print(f'-- Segment time: {pretty_time(segtime)} (raw {segtime})')
                print(f'-- Total time: {pretty_time(curtime)} (raw {curtime})')
            else:
                print('-- Resetting...')
                print('-- Current time: 0')
            progress = distance.ProfileProgress(profpath)
            timeoffset = progress.stats.modes_offline[9]
            curtime = 0
            started = False
            isfullrun = False

