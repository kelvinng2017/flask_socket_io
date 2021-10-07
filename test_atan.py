


import math
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

a=math.atan(1)
b=math.atan2(1,1)

kelvin_debug_log.logger.debug("a:"+str(a)+",b:"+str(b))

#垂直時
b=math.atan2(1,0)
kelvin_debug_log.logger.debug("b:"+str(b))

#弧度轉角度
b=math.atan2(1,0)
kelvin_debug_log.logger.debug("b:"+str(b/math.pi*180))