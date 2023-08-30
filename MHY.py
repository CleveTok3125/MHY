try:
    import requests, json, os

    try:
        dic_path = open('archive-mode', 'r').read()
        dic_f = open(dic_path, 'r').read()
        dic = json.loads(dic_f)
        game = dic['data']['game']
        latest = game['latest']
        diffs = game['diffs']
        latest_ver = latest['version'] + ' (archived)'
    except:
        api = "https://sdk-os-static.mihoyo.com/hk4e_global/mdk/launcher/api/resource?launcher_id=10&key=gcStgarh"
        try:
            r = requests.get(api)
        except:
            print("Unable to fetch URL")
            input("\nPress any key to exit...")
            exit()
        dic = json.loads((r).text)
        game = dic['data']['game']
        latest = game['latest']
        diffs = game['diffs']
        latest_ver = latest['version']


    def check_connection():
        os.system('cls')
        retcode = dic['retcode']
        mess = dic['message']

        if not retcode == 0 and mess == 'OK':
            print("Unable to fetch URL\n" + "Return code: " + retcode + "\n Message: " + mess)
            input("\nPress any key to exit...")
            exit()

    def latest_no_voice_packs():
        os.system('cls')
        size = str(round(int(latest['package_size']) / 1024**3, 2)) + 'GB'
        md5 = latest['md5']
        print("Download " + latest_ver + " (no voice packs)\nSize: " + size + "\nMD5: " + md5.upper() + "\n\nPress any key to download...")
        input("")
        return latest['path']

    def latest_voice_packs(mode):
        os.system('cls')
            # 0 Chinese
            # 1 English
            # 2 Japanese
            # 3 Korean
        voice_packs = latest['voice_packs']
        cdvoice = voice_packs[mode]
        size = str(round(int(cdvoice['package_size']) / 1024**3, 2)) + 'GB'
        md5 = cdvoice['md5']
        language = cdvoice['language']
        print("Download " + latest_ver + " (" + language.upper() + " voice pack)\nSize: " + size + "\nMD5: " + md5.upper() + "\n\nPress any key to download...")
        input("")
        return cdvoice['path']

    def latest_segments():
        os.system('cls')
        size = str(round(int(latest['package_size']) / 1024**3, 2)) + 'GB'
        print("Download " + latest_ver + " (no voice packs + segments)\nSize: " + size + "\n\nPress any key to show URL...")
        input("")
        for i in latest['segments']:
            md5 = i['md5']
            print("URL: " + i['path'] + "\nMD5: " + md5.upper() + "\n")
        print("Press any key to exit...")
        input("")
        exit()

    def diffs_no_voice_packs(mode):
        os.system('cls')
        size = str(round(int(diffs[mode]['package_size']) / 1024**3, 2)) + 'GB'
        md5 = diffs[mode]['md5']
        old_ver = diffs[mode]['version']
        print("Download " + old_ver + " to " + latest_ver + " (no voice packs)\nSize: " + size + "\nMD5: " + md5.upper() + "\n\nPress any key to download...")
        input("")
        return diffs[mode]['path']

    def diffs_voice_packs(mode, mode1):
        os.system('cls')
            # 0 Chinese
            # 1 English
            # 2 Japanese
            # 3 Korean
        old_ver = diffs[mode]['version']
        voice_packs = diffs[mode]['voice_packs']
        cdvoice = voice_packs[mode1]
        size = str(round(int(cdvoice['package_size']) / 1024**3, 2)) + 'GB'
        md5 = cdvoice['md5']
        language = cdvoice['language']
        print("Download " + old_ver + " to " + latest_ver + " (" + language.upper() + " voice pack)\nSize: " + size + "\nMD5: " + md5.upper() + "\n\nPress any key to download...")
        input("")
        return cdvoice['path']

    def folder_chooser():
        import win32gui
        from win32com.shell import shell, shellcon
        desktop_pidl = shell.SHGetFolderLocation (0, shellcon.CSIDL_DESKTOP, 0, 0)
        pidl, display_name, image_list = shell.SHBrowseForFolder (
          win32gui.GetDesktopWindow (),
          desktop_pidl,
          "Choose a folder",
          0,
          None,
          None
        )
        return os.path.normpath(str(shell.SHGetPathFromIDList(pidl))[2:-1])

    def download(link, path):
        from tqdm.auto import tqdm
        file = path + "\\" + link.split('/')[-1]
        response = requests.get(link, stream=True)
        with tqdm.wrapattr(open(file, "wb"), "write", miniters=1,
                           total=int(response.headers.get('content-length', 0)),
                           desc=file) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)

    def archive(latest_ver):
        os.system('cls')
        print("Latest version:", latest_ver)
        print("1. Archive this version")
        print("2. Change version")
        print("3. Exit archive mode\n")
        menu = int(input("Select one: "))

        if menu == 1:
            try:
                os.mkdir('archive')
            except:
                None

            content = requests.get(api, stream=True)
            open('archive/archive-'+str(latest_ver)+'.json', 'wb').write(r.content)
            input('Successfully archived: ' + '/archive/archive-'+str(latest_ver)+'.json')

        elif menu == 2:
            import easygui
            main_path = os.getcwd()
            os.chdir(main_path+'/archive')
            path = easygui.fileopenbox()
            os.chdir(main_path)

            open('archive-mode', 'w+').write(path)
            input('Changed to archive mode. Run again for changes.\n')
        elif menu == 3:
            try:
                os.remove('archive-mode')
            except:
                None
            input('Changed to normal mode. Run again for changes.\n')
            
        exit()

    check_connection()

    try:
        print("Pre-downloaded version!!\nPre-download version " + dic['data']['pre_download_game']['latest']['version'] + "\n")
        if input("Press U to switch to pre-download mode\nPress another key to return to the current version\n>>> ").lower() == "u":
            game = dic['data']['pre_download_game']
            latest = game['latest']
            diffs = game['diffs']
            latest_ver = latest['version']
        os.system('cls')
    except:
        None

    print("Latest version:", latest_ver)
    print("1. Get full", latest_ver)
    print("2. Update to", latest_ver)
    print("3. Update from an older version")
    print("4. Re-download resources")
    print("0. Open archiver\n")

    menu = int(input("Select one: "))
    if menu == 1:
        print("\n1. Base game")
        print("2. Voice packs")
        print("3. Segment download\n")
        menu1 = int(input("Select one: "))
        if menu1 == 1:
            url = latest_no_voice_packs()
        elif menu1 == 2:
            print("\n1. Chinese\n2. English\n3. Japanese\n4. Korean\n")
            url = latest_voice_packs(int(input("Select one: "))-1)
        elif menu1 == 3:
            latest_segments()
        else:
            input("Invalid selection\n")
            exit()
    elif menu == 2:
        print("\n1. Patch update")
        print("2. Voice packs update\n")
        menu1 = int(input("Select one: "))
        if menu1 == 1:
            url = diffs_no_voice_packs(0)
        elif menu1 == 2:
            print("\n1. Chinese\n2. English\n3. Japanese\n4. Korean\n")
            url = diffs_voice_packs(0, int(input("Select one: "))-1)
        else:
            input("Invalid selection\n")
            exit()
    elif menu == 3:
        print("\n1. Patch update")
        print("2. Voice packs update\n")
        menu1 = int(input("Select one: "))
        if menu1 == 1:
            url = diffs_no_voice_packs(1)
        elif menu1 == 2:
            print("\n1. Chinese\n2. English\n3. Japanese\n4. Korean\n")
            url = diffs_voice_packs(1, int(input("Select one: "))-1)
        else:
            input("Invalid selection\n")
            exit()
    elif menu == 4:
        import easygui, shutil, keyboard
        print("'Re-download resources' is a method of re-downloading the entire game content by scanning the game data map and downloading the necessary files to refresh. Only use to recover corrupted game data files, do not update new versions or restore missing or non-existent files in this way.\nMake sure the current installed game version is "+str(latest['version'])+"\nPress Enter key to continue")
        while True:
            if keyboard.is_pressed('enter'):
                os.system('cls')
                break
        org_dir = os.getcwd()
        game_dir = easygui.fileopenbox(msg='Select '+latest['entry']+' in game path', default=r'C:/Program Files/Genshin Impact/Genshin Impact game/', filetypes=['*.exe'])
        game_dir = os.path.split(game_dir)[0]
        os.chdir(game_dir)
        try:
            os.mkdir(os.path.join(os.getcwd(), '$temp'))
        except:
            None
        temp_game_dir = os.path.join(game_dir, '$temp')
        logs = []
        for dirname, dirnames, filenames in os.walk('.'):
            if '$temp' in dirnames:
                dirnames.remove('$temp')
            for filename in filenames:
                filepath = os.path.join(dirname, filename)
                dirs = filepath.replace('\\', '/')
                dir_link = (latest['decompressed_path'] + dirs).replace('ScatteredFiles./', 'ScatteredFiles/', 1)
                
                if requests.get(dir_link).status_code == 404:
                    None # Skip not found file(s)
                else:
                    temp_dir_game = (temp_game_dir + (dirs.replace('./', '\\', 1))).replace('/', '\\')
                    full_dir_game = (game_dir + (dirs.replace('./', '\\', 1))).replace('/', '\\')
                    temp_full_dir_game = temp_dir_game
                    temp_dir_game = os.path.split(temp_dir_game)[0]

                    try:
                        check_file_size = int(requests.get(dir_link, stream=True).headers['Content-length'])
                        if not os.path.exists(temp_dir_game):
                            try:
                                os.makedirs(temp_dir_game)
                            except:
                                None # just in case
                        download(dir_link, temp_dir_game)
                        local_file_size = int(os.path.getsize(temp_full_dir_game))

                        if local_file_size == check_file_size:
                            shutil.move(temp_full_dir_game, full_dir_game)
                        else:
                            in_log = {
                            'return message':'incomplete download file',
                            'file path': filepath,
                            'url': dir_link
                            }
                            logs.append(in_log)
                    except:
                        in_log = {
                        'return message':'file download failed',
                        'file path': filepath,
                        'url': dir_link
                        }
                        logs.append(in_log)
        shutil.rmtree(temp_game_dir)
        os.chdir(org_dir)
        if len(logs)>0:
            print('Complete! Press ESC to exit...\n'+str(logs))
        else:
            print('Complete! Press ESC to exit...')
        while True:
            if keyboard.is_pressed('esc'):
                break
        exit()
    elif menu == 0:
        archive(latest_ver)
    else:
        input("Invalid selection\n")
        exit()

    path = folder_chooser()
    '''
    print("Downloading...\nURL:", url)
    print()
    '''

    try:
        download(url, path)
    except:
        print('The file could not be downloaded, the link was removed, or the link could not be fetched due to publisher not uploading link for this item. Switch to archive mode to find available links.')
        print('Requested URL: "'+url+'"')
        input()
    exit()
except:
    None