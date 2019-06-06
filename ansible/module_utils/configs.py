def configs():
    return {
        "cluster_api_url": "https://cluster-api.seinternal.com/api/cluster/%s/",
        "lists": {
            "exim": ["local_domains", "mysql_logging_server", "managed_ips"],
            "caught": ["imap_host"],
            "api": ["mysql_server"],
            "archive": ["master"]
        },
        "services": {
            "filtering": {
                "method": "filter servers",
                "section": "exim",
                "option": "local_domains",
                "template": "Template Cluster filter",
                "lc_group": "Local Cloud Slaves",
                "hc_group": "Hosted Cloud Slaves",
                "list": True
            },
            "imap": {
                "method": "IMAP servers",
                "section": "caught",
                "option": "imap_host",
                "template": "Template Cluster quarantine",
                "lc_group": "Quarantine servers",
                "hc_group": "HC Quarantine Servers",
                "list": True
            },
            "logging": {
                "method": "logging servers",
                "section": "exim",
                "option": "mysql_logging_server",
                "template": "Template Cluster logging",
                "lc_group": "Logging servers",
                "hc_group": "Logging servers",
                "list": True
            },
            "master": {
                "method": "master",
                "section": "api",
                "option": "mysql_server",
                "template": "Template Cluster master",
                "lc_group": "Local Cloud Masters",
                "hc_group": "Local Cloud Masters",
                "list": False
            },
            "archive_master": {
                "method": "archive_master",
                "section": "archive",
                "option": "master",
                "template": "Template Cluster archive master",
                "lc_group": "Archive index",
                "hc_group": "Archive index",
                "list": True
            },
            "archive_index": {
                "method": "archive_master",
                "section": "archive",
                "option": "master",
                "template": "Template Cluster archive index",
                "lc_group": "Archive masters",
                "hc_group": "Archive masters",
                "list": True
            },
            "managed_ips": {
                "method": "additional names",
                "section": "exim",
                "option": "managed_ips",
                "list": True
            }

        }
    }
