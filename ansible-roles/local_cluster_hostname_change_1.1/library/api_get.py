#!/usr/bin/python

import requests
import json

def main():
    arguments = {
            "api_url"     : { "required": "True", "type": "str" },
            "select_key"  : { "required": "True", "type": "str" },
            "payload"     : { "required": "True", "type":"json" }
    }
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    api_url    = module.params['api_url']
    select_key = module.params['select_key']
    payload    = module.params['payload']
    
    headers    = {'Content-Type': 'application/json'}
    try:
        response = requests.get(api_url,headers=headers,data=payload)
        value    = json.loads(response.content)['result'][0][select_key]
    except Exception as e:
        module.fail_json(msg="exception={}".format(e))

    if module.check_mode:
       module.exit_json(changed=True)

    if not module.check_mode:
           module.exit_json(changed=True, value=value)


from ansible.module_utils.basic import *
main()
