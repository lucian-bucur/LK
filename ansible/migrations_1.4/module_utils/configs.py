def configs():
    return {
        "cluster_api_url": "https://cluster-api.seinternal.com/api/cluster/%s/",
        "lists": {
            "exim": ["local_domains", "mysql_logging_server", "managed_ips"],
            "caught": ["imap_host"]
        },
        "services": {
            "imap": {
                "method": "IMAP servers",
                "section": "caught",
                "option": "imap_host",
                "list": True
            },
            "master": {
                "method": "master",
                "section": "api",
                "option": "mysql_server",
                "list": False
            }
        }
    }