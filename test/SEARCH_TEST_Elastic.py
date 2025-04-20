
from elasticsearch import Elasticsearch

# 첫 ID는 'elastic'이며, 비밀번호는 처음 주어진 비밀번호를 변경가능함
ELASTIC_ID = "elastic"
ELASTIC_PASSWORD = "<password>"

# client instance 생성
client = Elasticsearch(
    "https://localhost:9200",   # endpoint
    ca_certs="/path/to/http_ca.crt",
    basic_auth=(ELASTIC_ID, ELASTIC_PASSWORD)
)

# 접속이 잘 되었다면 아래 코드로 확인가능함
client.info()