#!/usr/bin/python

import requests
import json
from requests.auth import HTTPBasicAuth

def main():
    arguments = {
            "api_url"        : { "required": True, "type": "str"                 },
            "payload"        : { "required": True, "type": "json"                },
            "username_auth"  : { "required": True, "type": "str"                 },
            "password_auth"  : { "required": True, "type": "str", "no_log": True }
    }
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    api_url       = module.params['api_url']
    payload       = module.params['payload']
    username_auth = module.params['username_auth']
    password_auth = module.params['password_auth']

    headers      = {'Content-Type': 'application/json'}
    try:
        response = requests.post(api_url,headers=headers,data=payload,auth=HTTPBasicAuth(username_auth, password_auth))
    except Exception as e:
        module.fail_json(msg="Error! code={}:message={}".format(type(e).__name__,str(e)))

    if module.check_mode:
       module.exit_json(changed=True)

    if not module.check_mode:
           module.exit_json(changed=True, value=response.content)


from ansible.module_utils.basic import *
main()
