from elasticsearch import Elasticsearch

class ElaGet():

    @classmethod
    def esObj(cls):
        es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
        return es