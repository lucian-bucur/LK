#!/usr/bin/python

import requests
import json

def main():
    arguments = {
            "api_url"   : { "required": True,   "type": "str" },
            "payload"   : { "required": "True", "type":"json" }
    }
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    api_url = module.params['api_url']
    payload = module.params['payload']

    headers    = {'Content-Type': 'application/json'}
    try:
        response = requests.get(api_url,headers=headers,data=payload)
        #appkey    = json.loads(response.content)['result']
    except Exception as e:
           module.fail_json(msg="Error! code={}:message={}".format(type(e).__name__,str(e)))

    if module.check_mode:
        module.exit_json(changed=True)

    if not module.check_mode:
        module.exit_json(changed=True, appkey='{}'.format(response.content))


from ansible.module_utils.basic import *
main()
