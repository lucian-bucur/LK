from cluster_api_service import ClusterApiService


service = ClusterApiService("test11.simplyspamfree.com")
service.get_cluster_conf()
service.add_imap_servers("server12.test11.simplyspamfree.com")