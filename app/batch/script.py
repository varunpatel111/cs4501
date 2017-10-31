from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = None
consumer = None
while consumer is None or es is None:
	try:
		consumer = KafkaConsumer('new-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
		es = Elasticsearch(['es'])
	except:
		pass

for listing in consumer:
	js = json.loads((listing.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=js["id"], body=js)
	es.indices.refresh(index="listing_index")
