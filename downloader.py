from ftplib import FTP
import os
from datetime import datetime as dt
import time

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

    already_downloaded_files = os.listdir(region_path)
    already_downloaded_files = [item + '.zip' if item[-3:] != 'zip' else item for item in already_downloaded_files]

    for file in ftp.nlst():
        if file in already_downloaded_files:
            continue

        file_to_download = os.path.join(region_path, file)
        with open(file_to_download, 'wb') as f:
            is_downloaded = False
            while not is_downloaded:
                try:
                    ftp.retrbinary('RETR ' + file, f.write)
                    is_downloaded = True
                except:
                    print('was unable to download', file, '. Sleeping for 10 seconds')
                    time.sleep(10)
        print('file', file, 'was downloaded at', dt.now())
