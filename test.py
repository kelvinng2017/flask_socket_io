import json
import os
import datetime
import show_and_save_log_file
f =open('./config.json','r')
data = json.load(f)
f.close()
log_file_path = data.get('log_file_path')
timeNow = datetime.datetime.now()
file_name_time = timeNow.strftime("%Y-%m-%d_%Hh%Mm%Ss")
if not os.path.exists(os.path.join(os.getcwd()+log_file_path)):
    print("creeate log file folder")
    os.makedirs(os.path.join(os.getcwd()+"/log/kelvinng_log_file/"))
file_name_path = os.getcwd()+log_file_path
kelvin_debug_log = show_and_save_log_file.Logger(file_name_path+""+os.path.basename(__file__)+"_"+file_name_time +
                                    ".log", level='debug')
kelvin_debug_log.logger.debug("hello")

test_list = ["a","b","c","d"]

kelvin_debug_log.logger.debug("ans:"+str(test_list[:1]))#從左邊讀取
kelvin_debug_log.logger.debug("ans:"+str(test_list[1:]))#抛棄右邊第一個
kelvin_debug_log.logger.debug("ans:"+str(test_list[-1-1]))