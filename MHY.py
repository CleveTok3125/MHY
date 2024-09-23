try:
    import requests, json, os
    global pre_download
    pre_download = False

    game_selector = ["Zenless Zone Zero", "Honkai: Star Rail", "Genshin Impact"]
    for i in range(len(game_selector)):
        print(f'{i+1}. {game_selector[i]}')

    game_selected = int(input("Select one: "))-1

    try:
        import re
        dic_path = open('archive-mode', 'r').read()
        dic_f = open(dic_path, 'r').read()
        invalid_chars = r'[\/:*?"<>|]'
        gn = game_selector[game_selected]
        gn = re.sub(invalid_chars, '', gn)
        if gn not in dic_path:
            raise ValueError("Not archived game")
        dic = json.loads(dic_f)
        game = dic['data']['game_packages'][game_selected]['main']
        latest = game['major']
        diffs = game['patches']
        latest_ver = latest['version'] + ' (archived)'
    except:
        api = "https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?launcher_id=VYTpXlbWo8"
        try:
            r = requests.get(api)
        except:
            print("Unable to fetch URL")
            input("\nPress any key to exit...")
            os._exit(0)
        dic = json.loads((r).text)
        game = dic['data']['game_packages'][game_selected]['main']
        latest = game['major']
        diffs = game['patches']
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
        # Due to the issue of large download size, some versions before 4.8 and later will no longer be able to download the entire client in one link.
        input("This feature is no longer available. Please use segment downloads instead.\n")
        os._exit(0)

    def latest_voice_packs(mode):
        os.system('cls')
            # 0 Chinese
            # 1 English
            # 2 Japanese
            # 3 Korean
        voice_packs = latest['audio_pkgs']
        cdvoice = voice_packs[mode]
        size = str(round(int(cdvoice['size']) / 1024**3, 2)) + 'GB'
        md5 = cdvoice['md5']
        language = cdvoice['language']
        print("Download " + latest_ver + " (" + language.upper() + " voice pack)\nSize: " + size + "\nMD5: " + md5.upper() + "\n")
        return cdvoice['url']

    def latest_segments():
        os.system('cls')
        print("Download " + latest_ver + " (no voice packs + segments)\n")
        list2download = []
        for i in latest['game_pkgs']:
            md5 = i['md5']
            size = i['size']
            url = i['url']
            list2download.append(url)
            print("File name: " + os.path.split(url)[-1] + "\nMD5: " + md5.upper() + "\nSize: " + str(round(int(size) / 1024**3, 2)) + 'GB' + "\n")
        return list2download

    def diffs_no_voice_packs(mode):
        os.system('cls')
        old_ver = diffs[mode]['version']
        print("Download " + old_ver + " to " + latest_ver + " (no voice packs + segments)\n")
        list2download = []
        for i in diffs[mode]['game_pkgs']:
            size = i['size']
            md5 = i['md5']
            url = i['url']
            list2download.append(url)
            print("File name: " + os.path.split(url)[-1] + "\nMD5: " + md5.upper() + "\nSize: " + str(round(int(size) / 1024**3, 2)) + 'GB' + "\n")
        return list2download

    def diffs_voice_packs(mode, mode1):
        os.system('cls')
            # 0 Chinese
            # 1 English
            # 2 Japanese
            # 3 Korean
        langlist = ['zh-cn', 'en-us', 'ja-jp', 'ko-kr']
        old_ver = diffs[mode]['version']
        voice_packs = diffs[mode]['audio_pkgs']
        for cdvoice in voice_packs:
            if langlist[mode1] == cdvoice['language']:
                break
            raise ValueError(f'Requested voice pack "{langlist[mode1]}" could not be found.')
        size = str(round(int(cdvoice['size']) / 1024**3, 2)) + 'GB'
        md5 = cdvoice['md5']
        language = cdvoice['language']
        print("Download " + old_ver + " to " + latest_ver + " (" + language.upper() + " voice pack)\nSize: " + size + "\nMD5: " + md5.upper() + "\n")
        return cdvoice['url']

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
            import re
            content = requests.get(api, stream=True)
            invalid_chars = r'[\/:*?"<>|]'
            gn = game_selector[game_selected]
            gn = re.sub(invalid_chars, '', gn)
            if pre_download:
                archive_path = 'archive/archive-'+gn+'_'+str(latest_ver)+'-predownload.json'
            else:
                archive_path = 'archive/archive-'+gn+'_'+str(latest_ver)+'.json'
            
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
        with open(data_structure_path, 'w+') as f:
            for item in data_structure:
                f.write("%s\n" % item)

        with open(os.path.join(game_dir, "deletefiles has been executed.txt"), "w+") as file:
            file.write('Do not delete this file as it is used to determine whether the default deletefiles.txt should be used. If this file exists, Game Patcher will automatically delete it and will not use deletefiles.txt to avoid conflicts with TH_GP.bat.')

        deletion_size = get_directory_size(des_folder)
        print('\nIn case files have been overwritten, it is possible to change the MHY version in the archiver to the previous version and use Re-download Resources to reverse the update.')
        print(f'Zip file structure: "{data_structure_path}"')
        input(f'Original size - Deletion size ≈ Remaining size\n{convert_size(original_size)} - {convert_size(deletion_size)} ≈ {convert_size(original_size-deletion_size)}\n')
        os._exit(0)

    def extract_zip(zip_file, extract_to):
        logs = []
        try:
            from tqdm import tqdm
            import zipfile, datetime
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                for member in tqdm(zip_ref.infolist(), desc="Extracting", unit="files"):
                    file_path = os.path.join(extract_to, member.filename)
                    size_file_path = -1
                    member_datetime = datetime.datetime(*member.date_time)
                    if os.path.exists(file_path):
                        size_file_path = os.path.getsize(file_path)
                        if (size_file_path != member.file_size) or (datetime.datetime.fromtimestamp(os.path.getctime(file_path)) < member_datetime):
                            with zip_ref.open(member) as source, open(file_path, 'wb') as target:
                                target.write(source.read())
                    else:
                        try:
                            os.makedirs(os.path.dirname(file_path))
                        except:
                            pass
                        with zip_ref.open(member) as source, open(file_path, 'wb') as target:
                            target.write(source.read())

                    if not ((os.path.exists(file_path))) or ((size_file_path != member.file_size) and (datetime.datetime.fromtimestamp(os.path.getctime(file_path)) < member_datetime)):
                        logs.append(file_path)
        except Exception as error:
            logs.append(file_path)
            print(error)
        return logs

    try:
        print("Pre-downloaded version!!\nPre-download version " + dic['data']['game_packages'][game_selected]['pre_download']['major']['version'] + "\n")
        if input("Press U to switch to pre-download mode\nPress another key to return to the current version\n>>> ").lower() == "u":
            game = dic['data']['game_packages'][game_selected]['pre_download']
            latest = game['major']
            diffs = game['patches']
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
    print("6. Unzip each file one by one")
    print("7. Game patch hdifffiles generator")
    print("8. Game patcher")
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
                    in_log = {
                    'return message':'file not found',
                    'file path': filepath,
                    'url': dir_link
                    }
                    logs.append(in_log)
                    print(in_log)
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
                                pass # just in case

                        if check_file_size == int(os.path.getsize(full_dir_game)): # Force redownload of duplicate files replaced with True
                            in_log = {
                            'return message':'Skip downloading duplicate files',
                            'file path': filepath,
                            'url': dir_link
                            }
                            logs.append(in_log)
                            print(in_log)
                        else:
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
                        print(in_log)
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
    elif menu == 6:
        import easygui
        print('Unzip each file one by one to minimize storage usage, ignore files of the same size and overwrite files of different sizes')
        zip_file = easygui.fileopenbox(msg='Select zip file', filetypes=['*.zip'])
        extract_to = folder_chooser()
        logs = extract_zip(zip_file, extract_to)
        if len(logs) > 0:
            print('List of files unpacking to the target directory failed:')
            for i in logs:
                print(i, end='\n')
        input('Zip extraction completed...\n')
        os._exit(0)
    elif menu == 7:
        import zipfile, easygui
        req = 0
        game_dir = 0
        game_vo_path = [0, 0, 0, 0]
        game_common_path = 0
        while True:
            os.system('cls')
            print("To run TH_GP.bat, you need Audio Common's hdifffiles.txt and one of the optional languages: Chinese, English, Japanese, Korean. This is a hdifffiles generator from a game data zip file.\nFor example: hdifffiles.txt from game_x.y.z_x.y.z_hdiff_RANDOMCODE.zip is Audio Common.\nhdifffiles.txt from en-us_x.y.z_x.y.z_hdiff_RANDOMCODE.zip is hdifffiles of the file containing the voiceover language.")
            print('Game path:', game_dir)
            print('AudioPatch path:', game_common_path)
            print('AudioPatch Language path:', game_vo_path)
            print('1. Select game path*')
            print('2. Select the game data update zip file*')
            print('3. Select the update language (Chinese) game data zip file')
            print('4. Select the update language (English) game data zip file')
            print('5. Select the update language (Japanese) game data zip file')
            print('6. Select the update language (Korean) game data zip file')
            print('0. Done')
            menu1 = int(input('Select one: '))
            if menu1 == 1:
                game_dir = easygui.fileopenbox(msg='Select game path', default=r'C:/Program Files/Genshin Impact/Genshin Impact game/', filetypes=['*.exe'])
                game_dir = os.path.split(game_dir)[0]
                req += 100
            elif menu1 == 2:
                game_common_path = easygui.fileopenbox(msg='Select the game data update zip file', filetypes=['*.zip'])
                req += 10
            elif menu1 == 3:
                game_vo_path[0] = easygui.fileopenbox(msg='Select the update language (Chinese) game data zip file', filetypes=['*.zip'])
                req += 1
            elif menu1 == 4:
                game_vo_path[1] = easygui.fileopenbox(msg='Select the update language (English) game data zip file', filetypes=['*.zip'])
                req += 1
            elif menu1 == 5:
                game_vo_path[2] = easygui.fileopenbox(msg='Select the update language (Japanese) game data zip file', filetypes=['*.zip'])
                req += 1
            elif menu1 == 6:
                game_vo_path[3] = easygui.fileopenbox(msg='Select the update language (Korean) game data zip file', filetypes=['*.zip'])
                req += 1
            elif menu1 == 0:
                if req >= 111 and game_common_path != 0 and game_dir != 0:
                    with zipfile.ZipFile(game_common_path, 'r') as zipf:
                        zipf.extract('hdifffiles.txt', game_dir)
                    input_file_path = os.path.join(game_dir, 'hdifffiles.txt')
                    output_file_path = os.path.join(game_dir, 'TH_GP_AudioPatch_Common.txt')
                    with open(input_file_path, 'r') as input_file:
                        content = input_file.read()
                        content = content.replace('{"remoteName": "', '')
                        content = content.replace('"}', '')
                        content = content.replace('/', '\\')
                    input_file.close()
                    with open(input_file_path, 'w+') as output_file:
                        output_file.write(content)
                    output_file.close()
                    if os.path.exists(output_file_path):
                        os.remove(output_file_path)
                    os.rename(input_file_path, output_file_path)
                    for i in range(0, len(game_vo_path)):
                        if game_vo_path[i] != 0:
                            with zipfile.ZipFile(game_vo_path[i], 'r') as zipf:
                                zipf.extract('hdifffiles.txt', game_dir)
                                if i == 0:
                                    new_name = 'TH_GP_AudioPatch_Chinese.txt'
                                elif i == 1:
                                    new_name = 'TH_GP_AudioPatch_English.txt'
                                elif i == 2:
                                    new_name = 'TH_GP_AudioPatch_Japanese.txt'
                                elif i == 3:
                                    new_name = 'TH_GP_AudioPatch_Korean.txt'
                                else:
                                    os._exit(403)
                            input_file_path = os.path.join(game_dir, 'hdifffiles.txt')
                            output_file_path = os.path.join(game_dir, new_name)
                            with open(input_file_path, 'r') as input_file:
                                content = input_file.read()
                                content = content.replace('{"remoteName": "', '')
                                content = content.replace('"}', '')
                                content = content.replace('/', '\\')
                            input_file.close()
                            with open(input_file_path, 'w+') as output_file:
                                output_file.write(content)
                            output_file.close()
                            if os.path.exists(output_file_path):
                                os.remove(output_file_path)
                            os.rename(input_file_path, output_file_path)
                    break
                else:
                    input('Items marked with * and one of 4 options 3-6 are required')
            else:
                input("Invalid selection\n")
        input('Completed.')
        os._exit(0)
    elif menu == 8:
        import zipfile, io, easygui, subprocess
        print('Use modified GenshinPatcher (source: https://github.com/GamerYuan/GenshinPatcher/) to patch game data.')
        game_dir = easygui.fileopenbox(msg='Select game path', default=r'C:/Program Files/Genshin Impact/Genshin Impact game/', filetypes=['*.exe'])
        game_dir = os.path.split(game_dir)[0]
        del_file1 = os.path.join(game_dir, 'deletefiles has been executed.txt')
        del_file2 = os.path.join(game_dir, 'deletefiles.txt')
        if os.path.exists(del_file1):
            try:
                print('Deleting deletefiles.txt...')
                os.remove(del_file2)
                os.remove(del_file1)
                print(f'Deleted successfully.\n{del_file2}\n{del_file1}')
            except:
                input(f'Delete failed. Please delete it manually and continue.\n{del_file2}\n{del_file1}')
        for i in ['TH_GP_AudioPatch_Chinese.txt', 'TH_GP_AudioPatch_English.txt', 'TH_GP_AudioPatch_English.txt', 'TH_GP_AudioPatch_Japanese.txt', 'TH_GP_AudioPatch_Korean.txt']:
            if (not os.path.exists(os.path.join(game_dir, 'TH_GP_AudioPatch_Common.txt'))) or (not os.path.exists(os.path.exists(os.path.join(game_dir, i)))):
                print('File hdifffiles not found. Please use Game patch hdifffiles generator to create.')
                os._exit(404)
        print('Downloading HDiffPatch (x64)...')
        api = 'https://api.github.com/repos/sisong/HDiffPatch/releases/latest'
        fetch = json.loads(requests.get(api).text)
        url = fetch['assets'][9]['browser_download_url']
        target_files = ["hdiffz.exe", "hpatchz.exe"]
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                for file_info in zip_ref.infolist():
                    file_name = os.path.basename(file_info.filename)
                    if file_name in target_files:
                        file_data = zip_ref.read(file_info.filename)
                        destination_file_path = os.path.join(game_dir, file_name)
                        with open(destination_file_path, 'wb') as destination_file:
                            destination_file.write(file_data)
                        print(f'File {file_name} has been moved to "{game_dir}"')
        else:
            print("Error downloading zip file: ", response.status_code)
            os._exit(0)
        api = 'https://raw.githubusercontent.com/CleveTok3125/MHY/main/TH_GP.bat'
        response = requests.get(api)
        if response.status_code == 200:
            with open(os.path.join(game_dir, 'TH_GP.bat'), 'wb') as file:
                file.write(response.content)
            print(f'File TH_GP.bat has been moved to "{game_dir}"')
        else:
            print("Error downloading zip file: ", response.status_code)
        print('Running TH_GP.bat...')
        subprocess.run([os.path.join(game_dir, 'TH_GP.bat')])
        input('Completed.')
        os._exit(0)
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
    except Exception as error:
        print('File could not be downloaded, link was removed, or the link could not be fetched due to publisher not uploading link for this item. Switch to archive mode to find available links.')
        print(f'Requested URL: {url}')
        print(f'For debugging: {error}')
        input()
    os._exit(0)
except Exception as error:
    print("\nEncountered an unexpected error:", error)