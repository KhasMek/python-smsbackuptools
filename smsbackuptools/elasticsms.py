#!/usr/bin/env python3

from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
import socket
from threading import Thread
import time


class QueueUpload(Thread):
   def __init__(self, queue):
       Thread.__init__(self)
       self.queue = queue

   def run(self):
       while True:
            message = self.queue.get()
            upload = Upload
            try:
                upload(message.tag, message.attrib)
            except AttributeError as err:
                print("{m} : {e}".format(m=message, e=err))
                pass
            self.queue.task_done()

class Upload():
    """ Upload class for elastic """
    def __init__(self, message_type, message):
        elastic_host = "localhost"
        elastic_port = "9200"
        index_name = "smsbackuprestore-"
        self.upload(elastic_host, elastic_port, index_name, message_type, message)

    def upload(self, elastic_host, elastic_port, index_name, message_type, message):
        es = Elasticsearch(host=elastic_host, port=elastic_port)
        pp = pprint.PrettyPrinter(indent=2, width=80, compact=True)
        create_body = es.index(index=index_name, doc_type=message_type, body=message)
        try:
            pp.pprint(create_body)
        except socket.timeout:
            print("SOCKET TIMEOUT: {m}".format(m=message.attrib))
            pass
        print("\n")
