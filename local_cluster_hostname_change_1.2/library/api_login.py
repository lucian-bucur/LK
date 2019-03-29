#!/usr/bin/python

import requests
import json
from ansible.module_utils.basic import *

def get_appkey(module,api_url,username,password):
    import requests
    import json
    headers = {'Content-Type': 'application/json'}
    payload = {
         "id": "1",
         "jsonrpc": "2.0",
         "method": "user.login",
         "params": {
             "user":     username,
             "password": password
         }
    }
    try:
       response         = requests.get(api_url,headers=headers,data=json.dumps(payload))
       response_content = json.loads(response.content)
       return response_content['result']
    except Exception as e:
        module.fail_json(msg="ExceptionType=[{}],ExceptionContent=[{}]".format(type(e), e))

def main():
    arguments = {
        "api_url"   : { "required": True, "type": "str"                 },
        "username"  : { "required": True, "type": "str"                 },
        "password"  : { "required": True, "type": "str", "no_log": True }
    }
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    api_url  = module.params['api_url']
    username = module.params['username']
    password = module.params['password']
    appkey   = get_appkey(module,api_url,username,password)

    if module.check_mode:
        module.exit_json(changed=True)

    if not module.check_mode:
        module.exit_json(changed=True, appkey='{}'.format(appkey))


if __name__=='__main__':
   main()
