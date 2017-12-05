from pyspark import SparkContext
import _mysql
import MySQLdb

sc = SparkContext("spark://spark-master:7077", "RecommendedItems")

data = sc.textFile("/tmp/data/accessLog.txt", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[0], pair[1])).distinct().join(pairs.map(lambda pair: (pair[0], pair[1])).distinct())
output = pages.map(lambda x: (x[1], x[0])).groupByKey()
output = output.map(lambda x: (x[0], len(x[1]))).filter(lambda x: list(x[0])[0] != list(x[0])[1]).filter(lambda x: x[1] > 2).collect()


for x in output:
    print (x[0][0] + ' and ' + x[0][1], (x[1]))

F = open("/tmp/data/sparkOutput.txt", 'w')

for x in output:
    F.write(str(x[0][0]) + ', ' + str(x[0][1]) + ': ' + str(x[1]) + "\n")

F.close()

print ("-----------------------------------------------")
print ("SPARK JOB DONE; NOW WRITING RECOMMENDATIONS INTO DATABASE")
print ("-----------------------------------------------")

sc.stop()

db=MySQLdb.Connection(host='db', user="www", passwd="$3cureUS", db="cs4501")

c = db.cursor()
#c.execute(""" DELETE FROM marketplace_recommendation; """)

d = {}

for x in output:
    l_1 = x[0][0]
    l_2 = x[0][1]

    l_1 = l_1.encode('ascii', 'ignore')
    l_2 = l_2.encode('ascii', 'ignore')

    curr_1 = d.get(l_1, '')
    curr_2 = d.get(l_2, '')

    if (curr_1 == ''):
        d[l_1] = str(l_2) + ', '
    else:
        if l_2 not in curr_1:
         d[l_1] = curr_1 + str(l_2) + ', '

    if (curr_2 == ''):
        d[l_2] = str(l_1) + ', '
    else:
        if l_1 not in curr_2:
         d[l_2] = curr_2 + str(l_1) + ', '

for key, value in d.items():
    c.execute(""" DELETE FROM marketplace_recommendation WHERE listing = (%s); """, (key))

for key, value in d.items():
    c.execute(""" INSERT INTO marketplace_recommendation (listing, listings) VALUES (%s, %s); """, (key, value))

db.commit()
db.close()

print ("-----------------------------------------------")
print ("RECOMMENDATIONS POPULATED INTO DATABASE; END OF SCRIPT")
print ("-----------------------------------------------")
