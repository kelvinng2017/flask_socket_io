import shutil
import os
import json


def delete_log_file():
    f =open('./config.json','r')
    data = json.load(f)
    f.close()
    log_file_path = data.get('log_file_path')


    try:
        shutil.rmtree(log_file_path)
        os.mkdir(log_file_path)

    except OSError as e:
        print(e.strerror)

delete_log_file()