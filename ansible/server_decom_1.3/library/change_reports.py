#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.reports import dumpx


def main():
    fields = {
        "domains":    {"default": True, "type": "list"},
        "interfaces": {"default": True, "type": "list"},
    }

    module     = AnsibleModule(argument_spec=fields)
    domains    = module.params["domains"]
    interfaces = module.params["interfaces"]
    result     = dumpx(domains,interfaces,key='address')

    module.exit_json(changed=True, value=result)


if __name__ == '__main__':
    main()
