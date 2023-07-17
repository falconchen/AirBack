#!/usr/bin/env python
from watchdog.observers import Observer
import sys
import os
import time
import logging
from Backuper import Backuper

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m')

    path = sys.argv[1] if len(sys.argv) > 1 else os.getenv('HOME') + os.sep + 'Downloads'

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
    except Exception as e:
        logging.error(f"An exception occurred: {str(e)}")

    observer.join()
