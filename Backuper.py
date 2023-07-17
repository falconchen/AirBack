# from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
from pathlib import Path
import time
import zipfile
import os


class Backuper(LoggingEventHandler):

    def __init__(self,watch_dir, video_dir, zip_dir,logger=None):
        # super().__init__()
        super().__init__(logger)
        self._watch_dir = watch_dir
        self._video_dir = video_dir
        self._zip_dir = zip_dir

        self.logger.info("watching dir: %s" % self._watch_dir)

    def on_moved(self, event):
        super().on_moved(event)
        self.backup(event.dest_path)

    # def on_deleted(self, event):
    #     pass

    def on_modified(self, event):
        super().on_modified(event)
        self.backup(event.src_path)

    def on_created(self, event):
        super().on_created(event)
        self.backup(event.src_path)

    def backup(self, file_path):
        
        src_path_obj = Path(file_path)
        if src_path_obj.stem[0] == '.':
          self.logger.warn(f"ignore hidden item: {file_path}")
          return False
        
        ext_name = src_path_obj.suffix

        if ext_name == '.':
          self.logger.warn(f"ignore hidden item: {file_path}")
          return False
        
        
        disallowed_exts = ('.crdownload','.bak','.tmp','.part')
        if ext_name in disallowed_exts:
            self.logger.warn(f"ignore disallowed extendsion name: {ext_name}")
            return False
    
        video_exts = ('.wmv', '.avi', '.mp4', '.mkv', '.rm',
                      '.rmvb', '.3gp', '.rm', '.mpeg', '.mpg', '.mov')

        if src_path_obj.parent.name == 'Youtube':
            backup_dir = self.create_time_dir()
            backup_path = Path(backup_dir).joinpath(src_path_obj.name)
        elif ext_name in video_exts:
            backup_dir = self.create_time_dir(self._video_dir)
            backup_path = file_path.replace(self._watch_dir, backup_dir)        
        else:
            backup_dir = self.create_time_dir()
            backup_path = file_path.replace(self._watch_dir, backup_dir)        

        
        backup_folder = Path(backup_path).parent
        if not Path(backup_folder).is_dir():
            os.makedirs(name=backup_folder,exist_ok=True)
        

        if src_path_obj.is_dir():
            os.makedirs(name=backup_path, exist_ok=True)
            return backup_path

        if not src_path_obj.exists():
            return backup_path

        try:
            if os.path.getsize(file_path) == 0:
                return backup_path
        except FileNotFoundError as e:
            self.logger.warn("Src File not Found: {src}".format(src=file_path))
            return False

        self.logger.info("start copy: from {src} to {target}".format(
            src=file_path, target=backup_path))

        fo = open(file_path, 'rb')
        content = fo.read()
        fo.close()

        fw = open(backup_path, 'wb')
        fw.write(content)
        fo.close()

        self.logger.info("copy done : {target}".format(target=backup_path))

        time.sleep(1)
        if os.path.getsize(file_path) == os.path.getsize(backup_path):
            self.logger.info(f"Del origin file: {file_path}")
            os.remove(file_path)

        if ext_name == ".zip":
            try:
                z_file = zipfile.ZipFile(backup_path, "r")

                extract_dir = self.create_time_dir()
                z_filelist = z_file.namelist()
                if len(z_filelist) > 0:
                    extract_dir = self.create_time_dir() + os.sep + Path(backup_path).stem

                os.makedirs(name=extract_dir, exist_ok=True)
                for filename in z_filelist:
                    self.logger.info("extracting {file} to {dir}".format(
                        file=filename, dir=extract_dir))
                    z_file.extract(filename, extract_dir)
                z_file.close()

                time.sleep(1)
                os.remove(backup_path)
                if os.path.exists(file_path):
                    os.remove(file_path)

            except Exception as e:
                self.logger.warning("exception happened:%s" % e)
                pass

        # print(f'{backup_path}')

    def create_time_dir(self, root=None):
        # 获取当前时间
        root = self._zip_dir if root is None else root
        time_now = time.strftime("%Y-%m-%d", time.localtime())
        path = root + os.sep + time_now
        # print(f"target: {path}")
        if not os.path.exists(path):
            os.makedirs(path)
            self.logger.info(f'created date directory:{path}')
        return path
