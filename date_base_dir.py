import os
import time
import shutil

# 遍历当前文件夹
for root,dirs,files in os.walk('./'):
  for f in files:
  # 获取文件创建时间
    ctime = os.path.getctime(os.path.join(root,f))
  # 根据创建时间，获取年月日
    date_dir = time.strftime('%Y-%m-%d',time.localtime(ctime))
  # 判断是否存在日期文件夹
  if not os.path.exists(date_dir):
  # 不存在，则新建
    os.makedirs(date_dir)
# 把文件转移到日期文件夹
shutil.move(os.path.join(root,f),os.path.join(date_dir,f))