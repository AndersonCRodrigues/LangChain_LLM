import weaviate


weaviate_client = weaviate.connect_to_local()
weaviate_client.close()
