import os
import shutil
import subprocess
import sys

import magic


def check_mime_types(directory):
    if not os.path.isdir(directory):
        return

    mime = magic.Magic(mime=True)
    mime_categories = {

        "image": "images",

        "video": "videos",

        "audio": "audio",

        "text": "documents",

        "application": "applications",

        "font": "fonts",

        "model": "3d_models"

    }

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.isfile(file_path):
                continue
            try:
                mime_type = mime.from_file(file_path)
                category = mime_type.split('/')[0]
                if category in mime_categories:
                    dest_folder = os.path.join(directory, mime_categories[category])
                else:
                    dest_folder = os.path.join(directory, "unknown")
                os.makedirs(dest_folder, exist_ok=True)
                file_ext = mime_type.split('/')[1].split(';')[0]
                new_file_name = f"{os.path.splitext(file)[0]}.{file_ext}"
                new_file_path = os.path.join(dest_folder, new_file_name)
                shutil.move(file_path, new_file_path)
            except Exception as e:
                pass


def collect_files(dest_directory, source_directories):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory, exist_ok=True)
    for src_dir in source_directories:
        if not os.path.isdir(src_dir):
            continue
        for root, _, files in os.walk(src_dir):
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_directory, file)
                counter = 1
                base, ext = os.path.splitext(file)
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_directory, f"{base}_{counter}{ext}")
                    counter += 1
                try:
                    shutil.copy2(src_path, dest_path)
                except Exception as e:
                    pass


def get_active_users():
    users = []
    if sys.platform.startswith("win"):
        try:
            active_sessions = subprocess.check_output("query user", shell=True).decode("cp866").split("\n")
            for session in active_sessions:
                parts = session.split()
                if len(parts) > 1 and parts[1] != 'USERNAME':
                    users.append(parts[0])
        except subprocess.CalledProcessError:
            users = [user for user in os.listdir("C:\\Users") if os.path.isdir(os.path.join("C:\\Users", user))]
    else:
        users = [user for user in os.listdir("/home") if os.path.isdir(os.path.join("/home", user))]
    print(f"Найденные пользователи: {"\n".join(users)}")
    return users


def get_home_directories():
    home_dirs = []
    active_users = get_active_users()
    if sys.platform.startswith("win"):
        for user in active_users:
            home_dirs.append(os.path.join("C:\\Users", user))
    else:
        for user in active_users:
            home_dirs.append(os.path.join("/home", user))
    return home_dirs


def get_browser_cache_dirs():
    cache_dirs = []
    browsers_list = []
    home_dirs = get_home_directories()
    for home in home_dirs:
        if sys.platform.startswith("win"):
            chrome_cache = os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data")
            edge_cache = os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data")
            firefox_profiles = os.path.join(home, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
            yandex_cache = os.path.join(home, "AppData", "Local", "Yandex", "YandexBrowser", "User Data")

            if os.path.exists(firefox_profiles):
                for profile in os.listdir(firefox_profiles):
                    cache_dirs.append(os.path.join(firefox_profiles, profile, "cache2", "entries"))
                browsers_list.append("Firefox")

            if os.path.exists(chrome_cache):
                for profile in os.listdir(chrome_cache):
                    cache_dirs.append(os.path.join(chrome_cache, profile, "Cache"))
                browsers_list.append("Chrome")

            if os.path.exists(edge_cache):
                for profile in os.listdir(edge_cache):
                    cache_dirs.append(os.path.join(edge_cache, profile, "Cache"))
                browsers_list.append("Edge")

            if os.path.exists(yandex_cache):
                for profile in os.listdir(yandex_cache):
                    cache_dirs.append(os.path.join(yandex_cache, profile, "Cache"))
                browsers_list.append("Yandex")
        else:
            firefox_profiles = os.path.join(home, ".cache", "mozilla", "firefox")
            chrome_cache = os.path.join(home, ".config", "google-chrome")
            yandex_cache = os.path.join(home, ".config", "yandex-browser")

            if os.path.exists(firefox_profiles):
                for profile in os.listdir(firefox_profiles):
                    cache_dirs.append(os.path.join(firefox_profiles, profile, "cache2", "entries"))
                browsers_list.append("Firefox")

            if os.path.exists(chrome_cache):
                for profile in os.listdir(chrome_cache):
                    cache_dirs.append(os.path.join(chrome_cache, profile, "Cache"))
                browsers_list.append("Chrome")

            if os.path.exists(yandex_cache):
                for profile in os.listdir(yandex_cache):
                    cache_dirs.append(os.path.join(yandex_cache, profile, "Cache"))
                browsers_list.append("Yandex")

    return (cache_dirs, browsers_list)


if __name__ == "__main__":
    print("""
    
 __ )                                   __ \ _)                       
 __ \   __| _ \\ \  \   / __|  _ \  __| |   | |  _` |  _` |  _ \  __| 
 |   | |   (   |\ \  \ /\__ \  __/ |    |   | | (   | (   |  __/ |    
____/ _|  \___/  \_/\_/ ____/\___|_|   ____/ _|\__, |\__, |\___|_|    
                                               |___/ |___/            
                                                   

             BrowserDigger 0.1 by NoneDev & NorthBear

========================================================================
""")
    if sys.platform.startswith("win"):
        temp_dir = "C:\\Temp\\browserdigger"
    else:
        temp_dir = "/tmp/browserdigger"
    cache_dir = os.path.join(temp_dir, "browser_cache")
    browser_cache_dirs, browsers_list = get_browser_cache_dirs()
    collect_files(cache_dir, browser_cache_dirs)
    print(f"\nАнализ информации из следующих браузеров:\n{"\n".join(set(browsers_list))}")
    check_mime_types(cache_dir)
    print("\nСбор окончен!")
