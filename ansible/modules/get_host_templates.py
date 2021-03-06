#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_service import ClusterApiService



def main():
    fields = {
        "host": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    host = module.params["host"]
    service = ClusterApiService(host)
    service.get_cluster_conf()
    result = service.get_host_templates(host)

    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
