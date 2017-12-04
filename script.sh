#!/usr/bin/env bash
docker exec -it spark-master bash
apt-get update
apt-get install python3-dev libmysqlclient-dev -y
apt-get install python-pip -y
pip install mysqlclient
apt-get install python-mysqldb
exit

docker exec -it spark-worker bash
apt-get update
apt-get install python3-dev libmysqlclient-dev -y
apt-get install python-pip -y
pip install mysqlclient
apt-get install python-mysqldb
exit

docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/sparkScript.py