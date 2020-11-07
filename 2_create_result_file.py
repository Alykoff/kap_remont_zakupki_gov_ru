import json
import os

save_dir_name = 'E:\\\\_tmp'


def find_all_files():
    for _, _, files in os.walk(save_dir_name):
        return files


def cat_all_links():
    files = find_all_files()
    result = []
    saved = set()
    for file in files:
        with open(save_dir_name + '\\' + file, 'r') as f:
            links = json.load(f)
            for el in links:
                if el in saved:
                    continue
                else:
                    saved.add(el)
                    result.append(el)
    with open(save_dir_name + '\\' + 'result.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return result


if __name__ == '__main__':
    cat_all_links()
