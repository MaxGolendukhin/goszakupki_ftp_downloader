from ftplib import FTP
import os
from datetime import datetime as dt
import time
import zipfile

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login(user='fz223free', passwd='fz223free')
ftp.cwd('/out/published/Moskva/purchaseNotice/daily/')
path = r'D:\Moskow'

files = ftp.nlst()
files.sort(reverse=True)

files_to_process = files.__len__()

already_downloaded_files = os.listdir(path)
already_downloaded_files = [path + '\\' + item for item in already_downloaded_files]

processed_files = 0
for file in files:
    file_to_download = os.path.join(path, file)

    if file_to_download in already_downloaded_files:
        continue

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

    folder_unzipped = os.path.join(path, 'unzipped')

    try:
        zip_ref = zipfile.ZipFile(file_to_download)  # create zipfile object
        zip_ref.extractall(folder_unzipped)  # extract file to dir
        zip_ref.close()  # close file
        print('file', file_to_download, 'uzipped at', dt.now())
    except:
        print('unable to unzip file', file_to_download)
        corrupted_files_folder = os.path.join(folder_unzipped, 'corrupted_files')
        if not os.path.exists(corrupted_files_folder):
            os.makedirs(corrupted_files_folder)
        os.rename(file_to_download, os.path.join(corrupted_files_folder, os.path.basename(file_to_download)))


    processed_files += 1
    print('Processed {:04.2f}%'.format(100.0 * processed_files / files_to_process))
