import requests
import json
from ansible.module_utils.config_loader import ConfigLoader
from ansible.module_utils.configs import configs


class ClusterApiService:
    user_agent = "manage_cluster.py"

    def __init__(self, host):
        self.domain = host.partition('.')[2]
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

    def get_servers_with_role(self, service_key):
        service = self.services.get(service_key)
        servers = self.config_loader.parser.get(service.get("section"), service.get("option"))
        return servers

    def get_host_templates(self,server):
        templates = ["Template Base", "Template Cluster base"]
        for key in self.services.keys():
            service = self.services.get(key)
            if server in self.config_loader.parser.get(service.get("section"), service.get("option")):
                templates.append(service.get("template"))
        return templates

    def get_host_groups(self,server):
        groups = ["All servers"]
        if "simplyspamfree.com" in server:
            groups.append("Development and testing servers")
        else:
            groups.append("All non-testing servers")
        if "antispamcloud.com" in server:
            groups.append("Hosted Cloud")
        for key in self.services.keys():
            service = self.services.get(key)
            if server in self.config_loader.parser.get(service.get("section"), service.get("option")):
                if "antispamcloud.com" in server:
                    groups.append(service.get("hc_group"))
                else:
                    groups.append(service.get("lc_group"))
        return groups

    def add(self, service_key, new_value):
        service = self.services.get(service_key)
        if service is None:
            raise Exception("Service %s is not know" % service_key)
        elif service.get("list") is False:
            raise Exception("Service %s values is not a list" % service_key)
        value = self.config_loader.parser.get(service.get("section"), service.get("option"))
        if new_value not in value:
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
        if new_value in value:
            value.remove(new_value)
        self.config_loader.parser.set(service.get("section"), service.get("option"), value)
        self.post(service)

    def modify(self, service_key, new_value):
        service = self.services.get(service_key)
        if service is None:
            raise Exception("Service %s is not know" % service_key)
        elif service.get("list") is False:
            value = new_value
        else:
            value = new_value.split(",")
        self.config_loader.parser.set(service.get("section"), service.get("option"), value)
        self.post(service)

    def replace(self, service_key, old_value, new_value):
        service = self.services.get(service_key)
        if service is None:
            raise Exception("Service %s is not know" % service_key)
        elif service.get("list") is False:
            raise Exception("Service %s values is not a list" % service_key)
        value = self.config_loader.parser.get(service.get("section"), service.get("option"))
        if new_value in value:
            value.remove(old_value)
            value.add(new_value)
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
