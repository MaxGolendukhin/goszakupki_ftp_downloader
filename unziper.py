import os
import glob
import zipfile
from datetime import datetime as dt

path = r'D:\purchase_notes'
for folder in glob.glob(path + '/*'):
    for file in glob.glob(os.path.join(path, folder) + '/*.zip'):
        try:
            zip_ref = zipfile.ZipFile(file)  # create zipfile object
            zip_ref.extractall(folder)  # extract file to dir
            zip_ref.close()  # close file
            os.remove(file)
            print('file', file, 'uzipped at', dt.now())
        except:
            print('unable to unzip file', file)
            unzipped_files_folder = os.path.join(folder, 'unzipped_files')
            if not os.path.exists(unzipped_files_folder):
                os.makedirs(unzipped_files_folder)
            os.rename(file, os.path.join(unzipped_files_folder, os.path.basename(file)))
