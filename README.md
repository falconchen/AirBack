# AirBack（备份Airdrop的文件到其他文件夹）

通过 Airdrop 的接收的文件只能存放在用户家目录的Download目录下，没有办法修改，如果经常使用，会在Download目录下产生大量杂乱文件。

这个脚本要做到的是：

0. 监控Mac下载目录的文件及目录（使用watchdog）
1. 把下载目录下的文件转移到备份的目录，如移动硬盘的某个目录，并且自动按添加日期建立该日期目录。
2. 视频文件备份到另外的目录
3. 自动解压zip到备份目录
4. 备份完成后，删除下载目录下的源文件

``` bash
pip install -r requirements.txt
./Airback.py
```
