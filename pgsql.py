import os
from subprocess import call

from helpers import log


def pg_system_db_backup(tmp_dir, username, port):
    log("PG system db backup started")

    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    postgres_system_config_file = tmp_dir + "/___system.sql.gz"
    log("\t- _SYSTEM_ > -%s" % postgres_system_config_file)

    os.popen("sudo -u %s pg_dumpall -p%s -g | gzip -9 -c > %s" % (
        username,
        port,
        postgres_system_config_file
    ))

    log("PG system db backup finished")


def pg_all_dbs_backup(tmp_dir, username, default_db, port):
    log("PG all db backup started")

    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    get_db_names = "sudo -u %s psql -d %s -p %s --tuples-only -c '\l' " \
                   "| awk -F\| '{ print $1 }' " \
                   "| grep -E -v '(template0|template1|^$)'" % (
                       username,
                       default_db,
                       port
                   )

    for base in os.popen(get_db_names).readlines():
        base = base.strip()

        if not base:
            continue

        filename = "%s/%s.sql.gz" % (tmp_dir, base)
        log("\t- %s > %s" % (base, filename), end='')
        call(
            "sudo -u %s pg_dump -C -F p -p%s %s | gzip -9 -c > %s" % (username, port, base, filename),
            shell=True)

        print(" (done) ")

    log("PG all db backup finished")
