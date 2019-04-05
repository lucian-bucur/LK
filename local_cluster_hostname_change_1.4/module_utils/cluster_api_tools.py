import json
import StringIO
import ConfigParser
import requests
from requests.auth import HTTPBasicAuth

USER_AGENT = "cluster_api_tools"

CONF = None

def load_configuration(server):
    requests.packages.urllib3.disable_warnings()
    result = requests.get('https://cluster-api.seinternal.com/api/cluster/%s/config/setup/' % \
                          server.partition('.')[2], verify=False)
    config = result.json()['configuration']
    buffer = StringIO.StringIO(config)
    conf = ConfigParser.ConfigParser()
    conf.readfp(buffer)
    return conf

def read_conf(server,section,item=None,force=False):
    global CONF
    if not CONF or force:
        CONF = load_configuration(server)
    if item:
        return CONF.get(section,item)
    return CONF.items(section)

def get_host_templates(server):
    roles = ["Template Base", "Template Cluster base"]
    if server in read_conf(server,"api","mysql_server"):
        roles.append("Template Cluster archive index")
    if server in read_conf(server,"archive","master"):
        roles.append("Template Cluster archive master")
    if server in read_conf(server,"exim","local_domains"):
        roles.append("Template Cluster filter")
    if server in read_conf(server,"exim","mysql_logging_server"):
        roles.append("Template Cluster logging")
    if server in read_conf(server,"caught","imap_host"):
        roles.append("Template Cluster quarantine")
    if server in read_conf(server,"api","mysql_server"):
        roles.append("Template Cluster master")
    if server in read_conf(server,"api","mysql_server"):
        roles.append("Template Cluster master API")
    return roles

def get_host_groups(server):
    groups = ["All servers"]
    if "simplyspamfree.com" in server:
        groups.append("Development and testing servers")
    else:
        groups.append("All non-testing servers")
    if "antispamcloud.com" in server:
        groups.append("Hosted Cloud")
        if server in read_conf(server,"caught","imap_host"):
            groups.append("HC Quarantine Servers")
        if server in read_conf(server,"exim","local_domains") and server not in read_conf(server,"api","mysql_server"):
            groups.append("Hosted Cloud Slaves")
    else:
        if  server in read_conf(server,"exim","local_domains") and server not in read_conf(server,"api","mysql_server"):
            groups.append("Local Cloud Slaves")
        if server in read_conf(server,"caught","imap_host"):
            groups.append("Quarantine servers")
    if server in read_conf(server,"api","mysql_server"):
        groups.append("Local Cloud Masters")
    if server in read_conf(server,"exim","mysql_logging_server"):
        groups.append("Logging servers")
    if server in read_conf(server,"api","mysql_server"):
        groups.append("Archive index")
    if server in read_conf(server,"archive","master"):
        groups.append("Archive masters")
    return groups

def change_master_servers(old_server,new_server):
    requests.packages.urllib3.disable_warnings()
    masters = read_conf(old_server,"api","mysql_server")
    if new_server not in masters:
        idata = masters.replace(old_server,new_server)
        prepared_data = {'master': json.dumps("%s") % idata}
        cluster = old_server.partition('.')[2]
        out = requests.post('https://cluster-api.seinternal.com/api/cluster/%s/' % \
                            cluster,data=prepared_data,headers={"User-Agent": USER_AGENT},verify=False)
        result = out.status_code
    else:
        result = "No changes!"
    return result

def change_imap_servers(old_server,new_server):
    requests.packages.urllib3.disable_warnings()
    imap_servers = read_conf(old_server,"caught","imap_host")
    if new_server not in imap_servers:
        idata = imap_servers.replace(old_server,new_server)
        prepared_data = {'IMAP servers': json.dumps(["%s"]) % idata}
        cluster = old_server.partition('.')[2]
        out = requests.post('https://cluster-api.seinternal.com/api/cluster/%s/' % \
                               cluster,data=prepared_data,headers={"User-Agent": USER_AGENT},verify=False)
        result = out.status_code
    else:
        result = "No Changes!"
    return result

def change_logging_servers(old_server,new_server):
    requests.packages.urllib3.disable_warnings()
    logging_servers = read_conf(old_server,"exim","mysql_logging_server")
    if new_server not in logging_servers:
        idata = logging_servers.replace(old_server,new_server)
        prepared_data = {'logging servers': json.dumps(["%s"]) % idata}
        cluster = old_server.partition('.')[2]
        out = requests.post('https://cluster-api.seinternal.com/api/cluster/%s/' % \
                               cluster,data=prepared_data,headers={"User-Agent": USER_AGENT},verify=False)
        result = out.status_code
    else:
        result = "No changes!"
    return result

def change_archive_master(old_server,new_server):
    requests.packages.urllib3.disable_warnings()
    archive_master = read_conf(old_server,"archive","master")
    if new_server not in archive_master:
        idata = archive_master.replace(old_server,new_server)
        prepared_data = {'archive master': json.dumps("%s") % idata}
        cluster = old_server.partition('.')[2]
        out = requests.post('https://cluster-api.seinternal.com/api/cluster/%s/' % \
                               cluster,data=prepared_data,headers={"User-Agent": USER_AGENT},verify=False)
        result = out.status_code
    else:
        result = "No changes!"
    return result

def change_filtering_servers(old_server,new_server):
    requests.packages.urllib3.disable_warnings()
    filtering_servers = read_conf(old_server,"exim","local_domains")
    if new_server not in filtering_servers:
        idata = filtering_servers.replace(old_server,new_server)
        prepared_data = {'filter servers': json.dumps(["%s"]) % idata}
        cluster = old_server.partition('.')[2]
        out = requests.post('https://cluster-api.seinternal.com/api/cluster/%s/' % \
                               cluster,data=prepared_data,headers={"User-Agent": USER_AGENT},verify=False)
        result = out.status_code
    else:
        result = "No changes!"
    return result
