#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_tools import get_host_templates


def main():
    fields = {
        "host": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    host= module.params["host"]
    result = get_host_templates(host)

    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
