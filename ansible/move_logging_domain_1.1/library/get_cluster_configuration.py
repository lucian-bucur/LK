#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_tools import load_configuration


def main():
    fields = {
        "host": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    host= module.params["host"]
    result = load_configuration(host)

    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
