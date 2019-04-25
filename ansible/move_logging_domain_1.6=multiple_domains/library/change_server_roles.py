#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_service import ClusterApiService

def main():
    fields = {
        "old_server": {"default": True, "type": "str"},
        "new_server": {"default": True, "type": "str"},
        "role": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    old_server = module.params["old_server"]
    new_server = module.params["new_server"]
    role = module.params["role"]
    service = ClusterApiService(old_server)
    service.get_cluster_conf()
    result = service.replace(role, old_server, new_server)
    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
