#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_tools import change_imap_servers


def main():
    fields = {
        "old_server": {"default": True, "type": "str"},
        "new_server": {"default": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    old_server = module.params["old_server"]
    new_server = module.params["new_server"]
    result = change_imap_servers(old_server,new_server)

    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
