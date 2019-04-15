import requests
import json
from config_loader import ConfigLoader


class ClusterApiService:
    user_agent = "manage_cluster.py"

    def __init__(self, domain):
        self.domain = domain
        self.url = "https://cluster-api.seinternal.com/api/cluster/%s/" % self.domain
        self.get_url = self.url + "config/setup/"
        self.config_loader = ""

    def get_cluster_conf(self):
        requests.packages.urllib3.disable_warnings()
        result = requests.get(self.get_url, verify=False)
        self.config_loader = ConfigLoader(result)
        self.config_loader.parse()

    def add_imap_servers(self, server):
        section = "caught"
        option = "imap_host"
        value = self.config_loader.parser.get(section, option)
        value.append(server)
        self.config_loader.parser.set(section, option, value)
        self.post(section, option, "IMAP servers")

    def remove_imap_servers(self, server):
        section = "caught"
        option = "imap_host"
        value = self.config_loader.parser.get(section, option)
        value.remove(server)
        self.config_loader.parser.set(section, option, value)
        self.post("IMAP servers", section, option)

    def post(self, section, option, method):
        requests.packages.urllib3.disable_warnings()
        data = {}
        data[method] = json.dumps(self.config_loader.parser.get(section, option))
        try:
            result = requests.post(self.url, data=data, headers = {"User-Agent": self.user_agent}, verify = False)
            print result
        except Exception as e:
            print e
