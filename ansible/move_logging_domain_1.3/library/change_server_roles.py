#!/usr/bin/env python

from ansible.module_utils.basic import *
from ansible.module_utils.cluster_api_tools import *

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
    if role == "quarantine":
        result = change_imap_servers(old_server,new_server)
    elif role == "logging":
        result = change_logging_servers(old_server,new_server)
    elif role == "master":
        result = change_master_servers(old_server,new_server)
    elif role == "archive_master":
        result = change_archive_master(old_server,new_server)
    elif role == "filter":
        result = change_filtering_servers(old_server,new_server)
    module.exit_json(changed=True, meta=result)


if __name__ == '__main__':
    main()
