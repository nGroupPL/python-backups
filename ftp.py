import ftplib
import os
from ftplib import FTP

from helpers import log


def _ftp_rm_tree(ftp, path):
    """Recursively delete a directory tree on a remote server."""
    wd = ftp.pwd()

    try:
        names = ftp.nlst(path)
    except ftplib.all_errors as e:
        log('\tCould not remove {0}: {1}'.format(path, e))
        return

    for name in names:
        if os.path.split(name)[1] in ('.', '..'): continue

        log('\tChecking {0}'.format(name))

        try:
            ftp.cwd(name)
            ftp.cwd(wd)
            _ftp_rm_tree(ftp, name)
        except ftplib.all_errors:
            ftp.delete(name)

    try:
        ftp.rmd(path)
    except ftplib.all_errors as e:
        log('\tCould not remove {0}: {1}'.format(path, e))


def _ftp_upload_files(ftp, path):
    for p in os.listdir(path):
        local_path = os.path.join(path, p)
        if os.path.isfile(local_path):
            log("\tSTOR %s %s" % (p, local_path))
            ftp.storbinary('STOR ' + p, open(local_path, 'rb'))
        elif os.path.isdir(local_path):
            log("\tMKD %s" % p)

            try:
                ftp.mkd(p)

            except ftplib.error_perm as e:
                if not e.args[0].startswith('550'):
                    raise

            log("\tCWD %s" % p)
            ftp.cwd(p)
            _ftp_upload_files(ftp, local_path)
            log("\tCWD ..")
            ftp.cwd("..")


def ftp_upload_files(tmp_dir, path, host, user, password):
    log("Send files to ftp")
    log("\tconnecting to host: %s" % host)
    ftp = FTP(host)
    log("\ttry to login")
    ftp.login(user, password)
    log("\tlogged in")

    ftp.cwd("~")
    for p in str(path).split('/'):

        try:
            log("\tftp cwd to %s" % p)
            ftp.cwd(p)
        except ftplib.error_perm:
            log("\ttmp path need doesn't exists, need to create it")
            ftp.mkd(p)
            ftp.cwd(p)
            log("\tcreated")

    log("\tlist files:")
    ftp.retrlines('LIST')

    log("\tstart upload")
    _ftp_upload_files(ftp, tmp_dir)

    log("\tquit")
    ftp.quit()


def ftp_clear(path, host, user, password):
    log("Send files to ftp")
    log("\tconnecting to host: %s" % host)
    ftp = FTP(host)
    log("\ttry to login")
    ftp.login(user, password)
    log("\tlogged in")

    try:
        log("\tftp cwd to %s" % path)
        ftp.cwd(path)
        dirs = set(ftp.nlst()) - {'.', '..'}
        dirs = sorted(dirs)

        for dir in dirs[:-2]:
            _ftp_rm_tree(ftp, dir)

    except ftplib.error_perm as e:
        print(e)

    ftp.quit()
