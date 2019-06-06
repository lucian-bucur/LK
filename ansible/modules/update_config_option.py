#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_service import ClusterApiService

def main():
    fields = {
        "server": {"default": True, "type": "str"},
        "value": {"default": True, "type": "str"},
        "key": {"default": True, "type": "str"},
        "action": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    server = module.params["server"]
    value = module.params["value"]
    key = module.params["key"]
    action = module.params["action"]
    service = ClusterApiService(server)
    service.get_cluster_conf()

    if action in ["add","remove","modify"]:
        result = getattr(service, action)(key, value)
    else:
        result = "Unknown action requested!"
    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
