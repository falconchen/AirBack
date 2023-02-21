from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
import zipfile
import os

class Backuper(FileSystemEventHandler):
  
    def __init__(self, watch_dir,video_dir, zip_dir):
      super(Backuper, self).__init__()      
      self._watch_dir = watch_dir
      self._video_dir = video_dir
      self._zip_dir = zip_dir
      print("watching dir: %s"%self._watch_dir)

    def on_moved(self, event):
        pass


    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        super(Backuper, self).on_modified(event)
        now_time = time.strftime("[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime())
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Modified : {2} ".format(now_time, what, event.src_path))
        self.backup(event.src_path)
        
    def on_created(self, event):
        #super(Backuper, self).on_create(event)
        now_time = time.strftime("[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime())
        what = 'directory' if event.is_directory else 'file'
        print ("{0} {1} Created : {2} ".format(now_time, what, event.src_path))
        self.backup(event.src_path)

    def backup(self,file_path):

        #file_path = '/Users/falcon/Downloads/新冠肺炎阳康一个月后，肺部恢复情况和我的后遗症【罗宾VLOG】-RIlNnh_m1t8.zip';                
        #self._video_dir = '/Volumes/Seagate/Share/115'

        ext_name = os.path.splitext(file_path)[-1]
        video_exts = ('.wmv','.avi','.mp4','.mkv','.rm','.rmvb','.3gp','.rm','.mpeg','.mpg','.mov')
        
        if ext_name in video_exts:                
          backup_dir = self.create_time_dir(self._video_dir)
        else:
          backup_dir = self.create_time_dir()

        backup_path = file_path.replace(self._watch_dir,backup_dir)

        
        #print(f"{file_path},{backup_path}")
        
        if os.path.isdir(file_path):
          os.makedirs(name=backup_path,exist_ok=True)
          return backup_path

        if not Path(file_path).exists() :
          return backup_path
        
        if os.path.getsize(file_path) == 0 :
          return backup_path

        print("start copy: from {src} to {target}".format(src=file_path,target=backup_path))

        fo = open(file_path,'rb')
        content = fo.read()
        fo.close()

        

        fw = open(backup_path,'wb')
        fw.write(content)
        fo.close()
        
        print("copy done : {target}".format(target=backup_path))

        time.sleep(1)
        if os.path.getsize(file_path) == os.path.getsize(backup_path):
          print(f"Del origin file: {file_path}")
          os.remove(file_path)

        if  ext_name == ".zip":
          try:
            z_file = zipfile.ZipFile(backup_path, "r")

            extract_dir = self.create_time_dir()
            z_filelist = z_file.namelist()
            if len(z_filelist) > 0 :
              extract_dir = self.create_time_dir() + os.sep + Path(backup_path).stem
            
            os.makedirs(name=extract_dir,exist_ok=True)
            for filename in z_filelist:
              print("extracting {file} to {dir}".format(file=filename,dir=extract_dir))
              z_file.extract(filename, extract_dir)
            z_file.close()

            time.sleep(1)
            os.remove(backup_path)
            if os.path.exists(file_path) :
              os.remove(file_path)

          except Exception as e:
            print("出现如下异常:%s"%e)
            pass


        print(f'{backup_path}')

  
    def create_time_dir(self,root=None):
        #获取当前时间
        root = self._zip_dir if root is None else root
        time_now = time.strftime("%Y-%m-%d", time.localtime())                
        path = root + os.sep + time_now
        print(f"target: {path}")
        if not os.path.exists(path):
            os.makedirs(path)
            print('文件夹创建完成  '+path)
        return path
