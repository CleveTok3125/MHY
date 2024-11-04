import os
import shutil
import subprocess

def check_files_exist(file_paths):
    missing_files = [file for file in file_paths if not os.path.exists(file)]
    return missing_files

def main():
    working_dir = os.path.dirname(os.path.abspath(__file__))
    audio_lang_file = os.path.join(working_dir, "ZenlessZoneZero_Data", "Persistent", "audio_lang")
    
    if not os.path.exists(audio_lang_file):
        print(f"Audio language file not found at {audio_lang_file}.")
        return

    languages = ['Zh', 'En', 'Ja', 'Ko']
    language_installed = {lang: False for lang in languages}
    file_missing = False
    current_language = None
    language_names = {
        'Zh': 'Chinese',
        'En': 'English',
        'Ja': 'Japanese',
        'Ko': 'Korean'
    }

    print("Checking if all necessary files to update the game from Patch are present...")
    
    with open(audio_lang_file, 'r') as f:
        for line in f:
            lang = line.strip()
            if lang in language_installed:
                language_installed[lang] = True
                current_language = language_names.get(lang)
                patch_file = os.path.join(working_dir, f"TH_GP_AudioPatch_{current_language}.txt")
                if not os.path.exists(patch_file):
                    print(f"{patch_file} is missing.")
                    file_missing = True

    common_patch_file = os.path.join(working_dir, "TH_GP_AudioPatch_Common.txt")
    if not os.path.exists(common_patch_file):
        print(f"{common_patch_file} is missing.")
        file_missing = True

    if file_missing:
        retry_query()
        return

    move_language_files(working_dir)
    
    if file_missing:
        retry_query()
        return
    
    apply_patch(working_dir, language_installed, language_names)
    cleanup(working_dir)

def move_language_files(working_dir):
    source = os.path.join(working_dir, "ZenlessZoneZero_Data", "Persistent", "Audio")
    target = os.path.join(working_dir, "ZenlessZoneZero_Data", "StreamingAssets", "Audio")
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target)

    print("Moved audio files to StreamingAssets.")

def apply_patch(working_dir, language_installed, language_names):
    print("Applying patches...")
    for lang, installed in language_installed.items():
        lang = language_names.get(lang)
        if installed:
            patch_file = os.path.join(working_dir, f"TH_GP_AudioPatch_{lang}.txt")
            with open(patch_file, 'r') as f:
                for line in f:
                    original_file = os.path.join(working_dir, line.strip())
                    patch_file = os.path.join(working_dir, f"{line.strip()}.hdiff")

                    if os.path.exists(original_file) and os.path.exists(patch_file):
                        subprocess.run(['hpatchz.exe', '-f', original_file, patch_file, original_file])
                    else:
                        print(f"{original_file} or {patch_file} is missing.")

    common_patch_file = os.path.join(working_dir, "TH_GP_AudioPatch_Common.txt")
    with open(common_patch_file, 'r') as f:
        for line in f:
            original_file = os.path.join(working_dir, line.strip())
            patch_file = os.path.join(working_dir, f"{line.strip()}.hdiff")

            if os.path.exists(original_file) and os.path.exists(patch_file):
                subprocess.run(['hpatchz.exe', '-f', original_file, patch_file, original_file])
            else:
                print(f"{original_file} or {patch_file} is missing.")

def cleanup(working_dir):
    print("Cleaning up obsolete files...")

def retry_query():
    selection = input("At least one file is missing. Retry patch application now? (y/n): ").strip().lower()
    if selection == 'y':
        main()
    else:
        print("Aborted patch application. Exiting.")

if __name__ == "__main__":
    main()