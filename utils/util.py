import time,datetime,json,os
from dateutil.relativedelta import relativedelta

import platform
from PIL import Image,ImageOps
import random
import subprocess
from utils.logger_settings import api_logger
import re
from urllib.parse import urlparse



# 常用工具
class Util:

  # 执行Linux命令
  def Exec(cmd: str):
    res = os.popen(cmd)
    return res.readlines()

  # 格式化时间
  def Date(format: str='%Y-%m-%d %H:%M:%S', timestamp: float=None):
    t = time.localtime(timestamp)
    return time.strftime(format, t)
  
  def DateFormat(format: str='%Y-%m-%d %H:%M:%S', duration: str='0s'):
    l = int(duration[:-1])
    r = duration[-1:]
    # 年、月、周、日、时、分、秒
    now = datetime.datetime.now()
    if r=='y' : d = now+relativedelta(years=l)
    elif r=='m' : d = now+relativedelta(months=l)
    elif r=='w' : d = now+relativedelta(weeks=l)
    elif r=='d' : d = now+relativedelta(days=l)
    elif r=='h' : d = now+relativedelta(hours=l)
    elif r=='i' : d = now+relativedelta(minutes=l)
    elif r=='s' : d = now+relativedelta(seconds=l)
    else : now+relativedelta(seconds=0)
    return d.strftime(format)

  # 时间戳
  def Time():
    return int(time.time())

  # String To Timestamp
  def StrToTime(day: str=None, format: str='%Y-%m-%d %H:%M:%S'):
    tArr = time.strptime(day, format)
    t = time.mktime(tArr)
    return t if t>0 else 0

  # Timestamp To GmtIso8601
  def GmtISO8601(timestamp: int):
    t = time.localtime(timestamp)
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", t)

  # 去首尾空格
  def Trim(content, charlist: str = None):
    text = str(content)
    return text.strip(charlist)

  # String to List
  def Explode(delimiter: str, string: str):
    return string.split(delimiter)

  # List to String
  def Implode(glue: str, pieces: list):
    return glue.join(pieces)

  # Array to String
  def JsonEncode(data):
    try :
      return json.dumps(data)
    except Exception as e :
      return ''

  # String to Array
  def JsonDecode(data: str):
    try :
      return json.loads(data)
    except Exception as e :
      return []

  # 合并数组
  def ArrayMerge(*arrays: dict):
    res = {}
    for arr in arrays :
      for k,v in arr.items() : res[k] = v
    return res

  # Url to Array
  def UrlToArray(url: str):
    if not url : return {}
    arr = url.split('?')
    path = arr[1] if len(arr)>1 else arr[0]
    arr = path.split('&')
    param = {}
    for v in arr :
      tmp = v.split('=')
      param[tmp[0]] = tmp[1]
    return param
  
  def is_folder(path):
    if os.path.exists(path) and os.path.isdir(path):
        return True
    else:
        return False   


  def createFolder(path):
   if not Util.is_folder(path):
       os.makedirs(path)

  def clearDir(path):
   # 删除文件夹中的所有文件
   for root, dirs, files in os.walk(path):
       for file in files:
           os.remove(os.path.join(root, file))

  def isStringInList(srcStr:str, inStrList):
      return any(srcStr in item for item in inStrList)
  

  def isMac():
    platform_ = platform.system()
    if platform_ == "Mac" or platform_ == "Darwin":
      return True
    
    return False


  def get_image_paths_from_folder(folder_path):
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    image_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for ext in image_extensions:
                if file.endswith(ext):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)

    return image_paths

  def resize_image(image_path, output_path, width, height):
    img = Image.open(image_path)
    saveImg = ImageOps.fit(img, (width,height))
    api_logger.info(f"原始尺寸{img.size}, fit后的尺寸{saveImg.size}")
    saveImg.save(output_path)


  def getRandomMp3FilePath(fromDir):
      mp3_files = [f for f in os.listdir(fromDir) if f.endswith(".mp3")]
      if not mp3_files:
          api_logger.info("No mp3 files found in the folder.")
          return ""
      else:
          random_mp3_file = random.choice(mp3_files)
          random_mp3_path = os.path.join(fromDir, random_mp3_file)
          api_logger.info(f"Random mp3 file: {random_mp3_path}")
          return random_mp3_path
      
  def getMediaDuration(filePath):
      try:
          cmd=f"ffprobe -i {filePath} -show_entries format=duration -v quiet -of csv=\"p=0\""
          result = subprocess.check_output(cmd, shell=True)
          durationFloat = float(result)
          return durationFloat
      except Exception as e:
          return 0

  def getRandomTransitionEffect():
      effects = ["DISSOLVE", "RADIAL", "CIRCLEOPEN", "CIRCLECLOSE", "PIXELIZE", "HLSLICE", 
              "HRSLICE", "VUSLICE", "VDSLICE", "HBLUR", "FADEGRAYS", "FADEBLACK", "FADEWHITE","RECTCROP",
              "CIRCLECROP", "WIPELEFT", "WIPERIGHT", "SLIDEDOWN", "SLIDEUP", "SLIDELEFT", "SLIDERIGHT"]
      return random.choice(effects).lower()
  

  def get_filename_and_extension(s):
    pattern = r'(\w+\.\w+)'
    match = re.search(pattern, s)
    if match:
        return match.group(1)
    else:
        return None
    
  def get_filename_and_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    filename_without_extension, file_extension = os.path.splitext(filename)
    return filename
