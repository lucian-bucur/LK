#!/usr/bin/env python

from __future__ import print_function

import sys
from zabbix_api import ZabbixAPI
import argparse
import json


class ZabbixService(object):
    def __init__(self):
        self.defaultgroup  = 'group_all'
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

        self.read_cli_args()

        if self.options.host:
            data = {'_meta': {'hostvars': {}}}
            print(json.dumps(data, indent=2))
        elif self.options.list:
            data = self.fetch_test_servers()
            print(data)
        else:
            print("usage: --list  ..OR.. --host <hostname>", file=sys.stderr)
            sys.exit(1)

    def fetch_groups(self,groupids):
        hosts = self.api.host.get({
            "output": "extend",
            "groupids": groupids
        })

        return json.dumps({
            "_meta": {'hostvars': {}},
            "group": {"hosts": list(map(lambda host: host['host'], hosts))}
        }, indent=2)

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.options = parser.parse_args()

    def fetch_hosted_cloud(self):
        return self.fetch_groups([8])

    def fetch_local_cloud(self):
        return self.fetch_groups([6, 7])

    def fetch_test_servers(self):
        return self.fetch_groups([12])

ZabbixService()
