import glob
import os
from ftplib import FTP
from datetime import datetime as dt

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login(user='fz223free', passwd='fz223free')
ftp.cwd('/out/published/')
path = r'D:\purchase_notes'

for region_path in glob.glob(path + '/*'):
    region = region_path.split('\\')[-1]
    for bad_file_path in glob.glob(os.path.join(region_path, 'unzipped_files') + '/*'):
        bad_file = bad_file_path.split('\\')[-1]

        with open(os.path.join(region_path, bad_file), 'wb') as f:
            file = '/out/published/' + region + '/purchaseNotice/daily/' + bad_file
            ftp.retrbinary('RETR ' + file, f.write)
            print('file', file, 'was downloaded at', dt.now())

        os.remove(bad_file_path)
