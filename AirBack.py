#!/usr/bin/env python
from watchdog.observers import Observer
import sys
import os
import time
from Backuper import Backuper

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.getenv(
        'HOME') + os.sep + 'Downloads'
    
    event_handler = Backuper(watch_dir=path,
                             video_dir='/Volumes/Seagate/Share/115',
                             zip_dir='/Volumes/Seagate/Share/Downloads')
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
