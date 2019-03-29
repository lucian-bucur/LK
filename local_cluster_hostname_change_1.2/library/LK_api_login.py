#!/usr/bin/python

import requests
import json

def main():
    arguments = {
            "api_url"   : { "required": True, "type": "str" }
             #"payload"   : { "required": True, "type":"json" }
    }
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    # api_url = module.params['api_url']
    # payload = module.params['payload']
    api_url = "https://monitor.seinternal.com/api_jsonrpc.php"
    payload = {
       "id": "1",
       "jsonrpc": "2.0",
       "method":  "user.login",
       "params": {
           "user":     "lucian.bucur",
           "password": "G5jINiSG7ekRwrSp"
       }
    }

    headers    = {'Content-Type': 'application/json'}
    value      = requests.get(api_url,headers=headers,data=json.dumps(payload))
    module.exit_json(changed=True, appkey = value )

    # if module.check_mode:
    #    module.exit_json(changed=True)
    #
    # if not module.check_mode:
    #        module.exit_json(changed=True, appkey = value)

from ansible.module_utils.basic import *
main()
