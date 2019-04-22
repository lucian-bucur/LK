import requests
import json
from config_loader import ConfigLoader
from configs import configs


class ClusterApiService:
    user_agent = "manage_cluster.py"

    def __init__(self, domain):
        self.domain = domain
        self.configs = configs()
        self.url = self.configs.get("cluster_api_url") % self.domain
        self.get_url = self.url + "config/setup/"
        self.services = self.configs.get("services")
        self.config_loader = ""

    def get_cluster_conf(self):
        requests.packages.urllib3.disable_warnings()
        result = requests.get(self.get_url, verify=False)
        self.config_loader = ConfigLoader(result)
        self.config_loader.parse()

    def add(self, service_key, new_value):
        service = self.services.get(service_key)
        if service is None:
            raise Exception("Service %s is not know" % service_key)
        elif service.get("list") is False:
            raise Exception("Service %s values is not a list" % service_key)
        value = self.config_loader.parser.get(service.get("section"), service.get("option"))
        value.append(new_value)
        self.config_loader.parser.set(service.get("section"), service.get("option"), value)
        self.post(service)

    def remove(self, service_key, new_value):
        service = self.services.get(service_key)
        if service is None:
            raise Exception("Service %s is not know" % service_key)
        elif service.get("list") is False:
            raise Exception("Service %s values is not a list" % service_key)
        value = self.config_loader.parser.get(service.get("section"), service.get("option"))
        value.remove(new_value)
        self.config_loader.parser.set(service.get("section"), service.get("option"), value)
        self.post(service)

    def modify(self, service_key, new_value):
        service = self.services.get(service_key)
        if service is None:
            raise Exception("Service %s is not know" % service_key)
        elif service.get("list") is True:
            raise Exception("Service %s value is not string" % service_key)
        value = self.config_loader.parser.get(service.get("section"), service.get("option"))
        value = new_value
        self.config_loader.parser.set(service.get("section"), service.get("option"), value)
        self.post(service)

    def post(self, role):
        requests.packages.urllib3.disable_warnings()
        data = {}
        data[role["method"]] = json.dumps(self.config_loader.parser.get(role["section"], role["option"]))
        try:
            result = requests.post(self.url, data=data, headers = {"User-Agent": self.user_agent}, verify = False)
            print result
        except Exception as e:
            print e
