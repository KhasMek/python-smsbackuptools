#!/usr/bin/env python3

import argparse
import os
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from datetime import datetime
from queue import Queue
from smsbackuptools.dbs import SQLite
from smsbackuptools.elasticsms import QueueUpload
from smsbackuptools.parser import ParseXML


def main():
    start_time = datetime.now()
    print("[I] START TIME: {t}".format(t=start_time))
    print("\n")
    parsexml = ParseXML()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-x', '--xml', default="sms.xml")
    argparser.add_argument('-e', '--elastic', action='store_true')
    argparser.add_argument('-s', '--sqlite', action='store_true')
    argparser.add_argument('-u', '--upload_threads', default="15")
    args = argparser.parse_args()
    xml = args.xml
    elastic = args.elastic
    sqlite = args.sqlite
    upload_threads = args.upload_threads
    try:
        tree = ET.parse(xml)
    except FileNotFoundError as err:
        print(err)
        print("[!] QUITTING!!!")
        sys.exit(1)
    except:
        print("\"{f}\" is malformed or not an xml!!!".format(f=xml))
        print("[!] QUITTING!!!")
        sys.exit(1)
    root = tree.getroot()
    if elastic:
        queueupload = QueueUpload
        queue = Queue()
        for x in range(int(upload_threads)):
            worker = queueupload(queue)
            worker.daemon = True
            worker.start()
        for message in root:
            message = parsexml.humanreadable(message)
            if message is not None:
                queue.put(message)
        queue.join()
    if sqlite:
        sqlite = SQLite()
        if os.stat("sbrt.db").st_size == 0:
            print("[I] DATABASE DOESN'T EXIST, CREATING...\n")
            sqlite.create_tables()
        for message in root:
            message = parsexml.humanreadable(message)
            sqlite.insert_row(message)
            sqlite.commit_db()
    else:
        parsexml.printall(root)
    end_time = datetime.now()
    print("[I] END TIME: {t}".format(t=end_time))
    print("[I] TOOK {t}".format(t=end_time - start_time))


if __name__ == "__main__":
    main()
