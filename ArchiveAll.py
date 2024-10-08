import requests, json, os, time
api = "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?launcher_id=VYTpXlbWo8"
try:
    os.mkdir('archive')
except:
    pass
game_selector = ["Zenless Zone Zero", "Honkai: Star Rail", "Genshin Impact"]
import re
content = requests.get(api, stream=True)
invalid_chars = r'[\/:*?"<>|]'
for game_selected in range(len(game_selector)):
    dic = json.loads((content).text)
    game = dic['data']['game_packages'][game_selected]['main']
    latest = game['major']
    diffs = game['patches']
    latest_ver = latest['version']
    pre_download = False
    try:
        game = dic['data']['game_packages'][game_selected]['pre_download']
        if len(game['patches']) != 0:
            pre_download = True
    except ValueError as e:
        input(e)
    gn = game_selector[game_selected]
    gn = re.sub(invalid_chars, '', gn)
    if pre_download:
        archive_path = 'archive/archive-'+gn+'_'+str(latest_ver)+'-predownload.json'
    else:
        archive_path = 'archive/archive-'+gn+'_'+str(latest_ver)+'.json'

    open(archive_path, 'wb').write(content.content)
    print('Successfully archived: ' + archive_path)
time.sleep(3)