from ftplib import FTP
import os
from datetime import datetime as dt
import glob

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login(user='fz223free', passwd='fz223free')
ftp.cwd('/out/published/')
path = r'D:\purchase_notes'

for region in ftp.nlst():
    region_path = os.path.join(path, region)
    if not os.path.exists(region_path):
        os.makedirs(region_path)

    try:
        ftp.cwd('/out/published/' + region + '/purchaseNotice/daily/')
    except:
        pass

    already_downloaded_files = glob.glob(region_path + '/*.zip')

    for file in ftp.nlst():
        file_to_download = os.path.join(region_path, file)
        if file_to_download in already_downloaded_files:
            continue

        with open(file_to_download, 'wb') as f:
            ftp.retrbinary('RETR ' + file, f.write)
        print('file', file, 'was downloaded at', dt.now())#.replace(microsecond=0))
