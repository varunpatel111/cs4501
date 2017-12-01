from kafka import KafkaConsumer

import json

consumer = None
while consumer is None:
	try:
		consumer = KafkaConsumer('clickedListings', group_id='clickedListing-indexer', bootstrap_servers=['kafka:9092'])
	except:
		pass

for click in consumer:
	js = json.loads((click.value).decode('utf-8'))
	F = open("accessLog.txt", 'a')
	F.write(str(js["user_id"]) + "," + str(js["listing_id"]) + "\n")
