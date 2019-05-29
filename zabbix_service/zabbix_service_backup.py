#!/usr/bin/env python

from __future__ import print_function

import sys
from zabbix_api import ZabbixAPI
import argparse
import json


class ZabbixService(object):
    def __init__(self):
        self.zabbix_server = 'https://monitor.seinternal.com'
        self.zabbix_username = 'ansible'
        self.zabbix_password = 'RGtfKgSc23q26f'
        self.zabbix_http_username = 'spam'
        self.zabbix_http_password = 'experts'

        try:
            self.api = ZabbixAPI(
                server=self.zabbix_server,
                user=self.zabbix_http_username,
                passwd=self.zabbix_http_password
            )
            self.api.login(self.zabbix_username, self.zabbix_password)
        except Exception as e:
            print("Error Logging In.", file=sys.stderr)
            sys.exit(1)

    def fetch_groups(self,groupids):
        hosts = self.api.host.get({
            "output": "extend",
            "groupids": groupids
        })
        return list(map(lambda host: host['host'], hosts))


    def fetch_hosted_cloud(self):
        data = self.fetch_groups([8])
        print(json.dumps(data, indent=2))

    def fetch_local_cloud(self):
        data = self.fetch_groups([6, 7])
        print(json.dumps(data, indent=2))

    def fetch_test_servers(self):
        return self.fetch_groups([12])


service = ZabbixService()
host_list = service.fetch_test_servers()
print(host_list)
