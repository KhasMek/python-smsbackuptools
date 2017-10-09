# Python SMSBackupRestore Tools

SMSBackupRestore Tools is meant to help with the interaction of backups from [_SMS Backup & Restore_](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore) by Carbonite.

**note:** I am not, nor have I ever been, affiliated with SMS Backup & Restore or Carbonite. I've only been a user of their program for a long time and sought a way to do something more with the data I've been collecting.

In this initial release, SMSBackuprestore Tools does two things -
- Print out the entire output of a xml file backed up by  _SMS Backup & Restore_.
- Upload the entirety of a xml file backed up by _SMS Backup & Restore_ to an Elasticsearch instance for viewing in Kibana (with example visualizations and dashboard).

More options for CLI based interaction should be coming soon. But, for now if one already has an ELK stack running, you can nerd out pretty good. This does work with both SMS's and MMS's, however their data is slightly different from one another (see [_type](#_type)).

---
### INSTALL

```
git clone https://github.com/KhasMek/python-smsbackuptools.git
pip install -r requirements.txt
```

By default, the elastic server is assumed to be localhost on port 9200. If your server is different, modify the `elastic_host` and `elastic_port` variables in `smsbackuptools/elasticsms.py`.

---
### RUN

To run with the default settings (using sms.xml as the source file, and printing the results to terminal) can be done by executing `./sbrt.py`. However, unless you replace the demo/testing sms.xml, this information will mean nothing. Additionally, I recommend piping most anything through less or something similar at this phase, otherwise you may be in for a bit of scrolling.

##### CLI FLAGS
| Short Flag |    Long Flag     | Default Value |                       Description                        |
| ---------- | ---------------- | ------------- | -------------------------------------------------------- |
| -x         | --xml            | sms.xml       | define an xml file to interact with                      |
| -e         | --elastic        | n/a           | upload to Elasticsearch                                  |
| -u         | --upload_threads | 15            | number of thread to use while uploading to Elasticsearch |
| -s         | --sqlite         | n/a           | create/update a sqlite database located at `./sbrt.db`   |

To upload my-sms.xml to a local Elasticsearch instance while saving the output to output.txt
```bash
./sbrt.py -e -x my-sms.xml >> output.txt
```

---
### ELASTICSEARCH & KIBANA

This is a incredibly easy way to dig through data backed up by _SMS Backup & Restore_ to find out the most random of likely pointless information. In the `examples` directory, there is a saved dashboard for Kibana along with the necessary visualizations needed. This should be a solid start for anyone curious about visualizing any of their data. Contributions welcome!

---
### TODO

- [ ] ingest to db.
- [ ] upload newly ingested from db to elastic.
- [ ] remove duplicates and export clean xml.
- [ ] search and sort by attribute.
- [x] Elasticsearch: account for mms message formatting.
- [ ] mms sent/received type(?)

---
### ATTRIBUTES

##### _type

|      MMS      |      SMS       |
| :-----------: | :------------: |
|    address    | readable_date  |
|    creator    |      body      |
|     m_size    |  contact_name  |
|      ct_l     |      date      |
|       v       |    address     |
|  retr_txt_cs  |      read      |
|       rr      |     status     |
| readable_date |      type      |
|     rpt_a     | service_center |
|     m_type    |      toa       |
|    resp_st    |    subject     |
|    retr_st    |    protocol    |
|      seen     |   date_sent    |
|     m_cls     |     locked     |
|      pri      |     sc_toa     |
|     tr_id     |                |
|       st      |                |
|   text_only   |                |
|      m_id     |                |
|    msg_box    |                |
|      ct_t     |                |
|      sub      |                |
|      text     |                |
|     sub_id    |                |
|    retr_txt   |                |
|     sub_cs    |                |
|    resp_txt   |                |
|      read     |                |
|     d_rpt     |                |
|     ct_cls    |                |
|   attachment  |                |
|   date_sent   |                |
|      exp      |                |
|     locked    |                |
|      date     |                |
|  contact_name |                |
|      d_tm     |                |
|  read_status  |                |

---
