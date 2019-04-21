#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_tools import get_servers_with_role


def main():
    fields = {
        "host": {"default": True, "type": "str"},
        "role": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    host= module.params["host"]
    role= module.params["role"]
    result = get_servers_with_role(host,role)

    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
