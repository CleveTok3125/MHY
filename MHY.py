try:
    import requests, json, os
    global pre_download
    pre_download = False

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
            os._exit(0)
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
            os._exit(0)

    def latest_no_voice_packs():
        os.system('cls')
        size = str(round(int(latest['package_size']) / 1024**3, 2)) + 'GB'
        md5 = latest['md5']
        print("Download " + latest_ver + " (no voice packs)\nSize: " + size + "\nMD5: " + md5.upper() + "\n")
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
        print("Download " + latest_ver + " (" + language.upper() + " voice pack)\nSize: " + size + "\nMD5: " + md5.upper() + "\n")
        return cdvoice['path']

    def latest_segments():
        os.system('cls')
        size = str(round(int(latest['package_size']) / 1024**3, 2)) + 'GB'
        print("Download " + latest_ver + " (no voice packs + segments)\nSize: " + size + "\n")
        list2download = []
        for i in latest['segments']:
            md5 = i['md5']
            url = i['path']
            list2download.append(url)
            print("File name: " + os.path.split(url)[-1] + "\nMD5: " + md5.upper() + "\n")
        return list2download

    def diffs_no_voice_packs(mode):
        os.system('cls')
        size = str(round(int(diffs[mode]['package_size']) / 1024**3, 2)) + 'GB'
        md5 = diffs[mode]['md5']
        old_ver = diffs[mode]['version']
        print("Download " + old_ver + " to " + latest_ver + " (no voice packs)\nSize: " + size + "\nMD5: " + md5.upper() + "\n")
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
        print("Download " + old_ver + " to " + latest_ver + " (" + language.upper() + " voice pack)\nSize: " + size + "\nMD5: " + md5.upper() + "\n")
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

    def download(input_link, path):
        from tqdm.auto import tqdm
        def downloader(link, path):
            file = path + "\\" + link.split('/')[-1]
            response = requests.get(link, stream=True)
            with tqdm.wrapattr(open(file, "wb"), "write", miniters=1,
                               total=int(response.headers.get('content-length', 0)),
                               desc=file) as fout:
                for chunk in response.iter_content(chunk_size=4096):
                    fout.write(chunk)

        if type(input_link) == list:
            for link in input_link:
                downloader(link, path)
        else:
            downloader(input_link, path)

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
                pass

            content = requests.get(api, stream=True)
            if pre_download:
                archive_path = 'archive/archive-'+str(latest_ver)+'-predownload.json'
            else:
                archive_path = 'archive/archive-'+str(latest_ver)+'.json'
            
            open(archive_path, 'wb').write(r.content)
            input('Successfully archived: ' + archive_path)

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
            
        os._exit(0)

    def downloadwithdownloader(url):
        import easygui
        downloader_path = easygui.fileopenbox(msg='Select downloader', filetypes=['*.exe'])
        if type(url) == list:
            os.system("start " + downloader_path + " " + " ".join(url))
        else:
            os.system("start " + downloader_path + " " + url)

    check_connection()

    def get_directory_size(directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size

    def convert_size(size_bytes):
        import math
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def delete_files():
        import easygui, zipfile
        print('Use deletefiles.txt to move files that need to be deleted to a new path while keeping the directory structure and create a list of files in the zip file for the update reversal process.')
        org_dir = os.getcwd()
        game_dir = easygui.fileopenbox(msg='Select game path', default=r'C:/Program Files/Genshin Impact/Genshin Impact game/', filetypes=['*.exe'])
        game_dir = os.path.split(game_dir)[0]
        game_del_path = easygui.fileopenbox(msg='Select the game data update zip file', filetypes=['*.zip'])
        original_size = get_directory_size(game_dir)
        os.chdir(game_dir)
        des_folder = os.path.join(os.getcwd(), os.path.normpath('$deletefiles'))
        try:
            os.mkdir(des_folder)
        except:
            pass
        os.chdir(org_dir)

        with zipfile.ZipFile(game_del_path, 'r') as zip_ref:
            data_structure = zip_ref.namelist()
            if 'deletefiles.txt' in data_structure:
                with zip_ref.open('deletefiles.txt') as file:
                    text_content = file.read().decode('utf-8')
                    text_content = text_content.split('\n')
                    for file_path in text_content:
                        rel_file_path = os.path.normpath(file_path)
                        file_path = os.path.join(game_dir, rel_file_path)
                        try:
                            des_path = os.path.join(des_folder, rel_file_path)
                            try:
                                os.makedirs(os.path.dirname(des_path))
                            except:
                                pass
                            os.rename(file_path.strip(), des_path.strip())
                            print(f"Moved {file_path} to {des_path}")
                        except Exception as error:
                            print(error)
            else:
                input("File 'deletefiles.txt' does not exist in the zip file.")
                os._exit(404)

        data_structure_path = os.path.join(des_folder, os.path.normpath(f'{os.path.split(game_del_path)[-1]}.txt'))
        with open(data_structure_path, 'w') as f:
            for item in data_structure:
                f.write("%s\n" % item)

        deletion_size = get_directory_size(des_folder)
        print('\nIn case files have been overwritten, it is possible to change the MHY version in the archiver to the previous version and use Re-download Resources to reverse the update.')
        print(f'Zip file structure: "{data_structure_path}"')
        input(f'Original size - Deletion size ≈ Remaining size\n{convert_size(original_size)} - {convert_size(deletion_size)} ≈ {convert_size(original_size-deletion_size)}\n')
        os._exit(0)
    try:
        print("Pre-downloaded version!!\nPre-download version " + dic['data']['pre_download_game']['latest']['version'] + "\n")
        if input("Press U to switch to pre-download mode\nPress another key to return to the current version\n>>> ").lower() == "u":
            game = dic['data']['pre_download_game']
            latest = game['latest']
            diffs = game['diffs']
            latest_ver = latest['version']
            pre_download = True
        os.system('cls')
    except:
        pass

    print("Latest version:", latest_ver)
    print("1. Get full", latest_ver)
    print("2. Update to", latest_ver)
    print("3. Update from an older version")
    print("4. Re-download resources")
    print("5. Execute deletefiles.txt")
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
            url = latest_segments()
        else:
            input("Invalid selection\n")
            os._exit(0)
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
            os._exit(0)
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
            os._exit(0)
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
            pass
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
        os._exit(0)
    elif menu == 5:
        delete_files()
    elif menu == 0:
        archive(latest_ver)
    else:
        input("Invalid selection\n")
        os._exit(0)

    '''
    print("Downloading...\nURL:", url)
    print()
    '''

    try:
        menu = int(input("1. Use built-in downloader\n2. Use 3rd party downloader\n3. Show URL(s)\nSelect one: "))
        if menu == 1:
            path = folder_chooser()
            download(url, path)
        elif menu == 2:
            downloadwithdownloader(url)
            input()
        elif menu == 3:
            if type(url) == list:
                for i in url:
                    print(i)
            else:
                print(url)
            input()
        else:
            input("Invalid selection\n")
            os._exit(0)
    except:
        print('The file could not be downloaded, the link was removed, or the link could not be fetched due to publisher not uploading link for this item. Switch to archive mode to find available links.')
        print('Requested URL: "'+url+'"')
        input()
    os._exit(0)
except Exception as error:
    print(error)