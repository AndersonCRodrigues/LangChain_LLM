import weaviate
from weaviate.connect import ConnectionParams, ProtocolParams


# weaviate_client = weaviate.connect_to_local(
#     host="127.0.0.1",
#     port=8080,
#     grpc_port=50051,
# )

# print("Conectado ao Weaviate!")

# weaviate_client.close()
http_params = ProtocolParams(
    host="localhost",
    port=8080,  # Defina a porta HTTP
    secure=False,  # Defina para False se não for uma conexão segura (HTTPS)
)

grpc_params = ProtocolParams(
    host="localhost",
    port=50051,  # Defina a porta GRPC
    secure=False,  # Defina para False se não for uma conexão segura
)

connection_params = ConnectionParams(http=http_params, grpc=grpc_params)

weaviate_client = weaviate.WeaviateClient(connection_params=connection_params)
weaviate_client.connect()
