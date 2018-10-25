import os
import tarfile

from helpers import log


def file_backup(tmp_dir, paths):

    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    log("File backups started")
    for name in paths:
        tar_filename = tmp_dir + "/" + (name[1:].replace('/', '_')) + ".tar.gz"
        log("\t- %s > %s" % (name, tar_filename), end=' ')
        tar = tarfile.open(tar_filename, "w:gz")
        tar.add(name)
        tar.close()
        print(" (done) ")

    log("File backups created")
