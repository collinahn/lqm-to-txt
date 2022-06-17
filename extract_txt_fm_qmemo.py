'''
파일과 같은 위치에 있는 lqm 파일들을 zip으로 바꾸고, 
zip 파일 속의 jlqm 파일들을 추출하여 json 파일로 뽑아낸 뒤 
텍스트 부분을 추출하여 순서대로 개별 파일에 저장한다.
'''

import os 
import zipfile
import shutil
import json

LG_QMEMO_EXT = '.lqm'
ZIP_FILE_EXT = '.zip'
TARGET_FILE = 'memoinfo.jlqm'
RESULT_DIR = './results'
folders = []

file_list = os.listdir()
for file in file_list:
    if file.endswith(LG_QMEMO_EXT):
        os.rename(file, f'{file.split(".")[0]}.zip')

zip_file_list = os.listdir()
print(zip_file_list)
for file in zip_file_list:
    if not file.endswith(ZIP_FILE_EXT):
        continue

    fzip = zipfile.ZipFile(file)
    
    folder_name = file.split('.')[0]
    folders.append(folder_name)

    if os.path.exists(folder_name):
        continue
    os.makedirs(folder_name)
    fzip.extract(TARGET_FILE, f'./{folder_name}')

if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)
    
for idx, folder in enumerate(folders):
    if os.path.exists(f'./{folder}/{TARGET_FILE}'):
        shutil.move(f'./{folder}/{TARGET_FILE}', f'{RESULT_DIR}/{idx}.json')

    with open(f'{RESULT_DIR}/{idx}.json', 'r', encoding='utf-8') as json_file:
        dct_object = json.load(json_file)
    
    content = dct_object['MemoObjectList'][0]['DescRaw']

    with open(f'{RESULT_DIR}/{idx}.txt', 'w', encoding='utf-8') as f:
        f.write(content) 
    with open(f'{RESULT_DIR}/total.txt', 'a', encoding='utf-8') as f:
        f.write(content)
        f.write('\n\n') 

    os.remove(f'{RESULT_DIR}/{idx}.json')