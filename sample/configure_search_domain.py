import rubrik_cdm

rubrik = rubrik_cdm.Connect()

search_domains = ["python.lab", "go.lab"]
cluster_search_domains = rubrik.cluster_search_domain(search_domains)
