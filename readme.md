```
import datetime
import os
import shutil

from file import file_backup
from ftp import ftp_upload_files, ftp_clear
from helpers import log
from pgsql import pg_system_db_backup, pg_all_dbs_backup

backup_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
tmp_dir = "/var/tmp/{}".format(backup_name)

log("Temporary directory: %s" % tmp_dir)

if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)

os.mkdir(tmp_dir)

file_backup(tmp_dir + "/files", ['/etc/apache2', '/home'])
pg_system_db_backup(tmp_dir + "/pg", 'postgres', 5432)
pg_all_dbs_backup(tmp_dir + "/pg", 'postgres', 'postgres', 5432)
ftp_upload_files(tmp_dir, path='backup/{}'.format(backup_name), host='', user='', password='')
ftp_clear(path='', host='', user='', password='')

log("Cleanup")
shutil.rmtree(tmp_dir)
```