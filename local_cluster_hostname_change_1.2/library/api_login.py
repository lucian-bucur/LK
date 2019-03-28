#!/usr/bin/python

import requests
import json

def get_appkey(module,api_url,username,password):
    import requests
    import json
    headers = {'Content-Type': 'application/json'}
    payload = {
         "jsonrpc": "2.0",
         "method": "user.login",
         "params": {
             "user":     username,
             "password": password
         },
         "id": 1
    }
    try:
           response         = requests.get(api_url,headers=headers,json=payload)
           response_content = json.loads(response.content)
           return response_content['result']
    except Exception as e:
        module.fail_json(msg="Error! code={}:message={}".format(type(e).__name__,str(e)))


def main():
    arguments = dict(
            api_url  = dict(required=True),
            username = dict(required=True),
            password = dict(required=True, no_log=True)
        )
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    api_url=module.params['api_url']
    username=module.params['username']
    password=module.params['password']
    appkey=get_appkey(module,api_url,username,password)

    if module.check_mode:
        module.exit_json(changed=True)

    if not module.check_mode:
        module.exit_json(changed=True, appkey='{}'.format(appkey))


from ansible.module_utils.basic import *
main()
