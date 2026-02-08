#READ and Write
# Import SQLContext do modulo pyspark.sql
from  pyspark.sql import SQLContext

# Inicia SparkContext localmente com 3 nucleos
# Os arquitvos poderam ser processados em 3 nodes paralelos
#sc = SparkContext()

# Cria SQLContext no SparkContext
sqlContext = SQLContext(sc)

# Comando para ler arquivo TXT e converter em um RDD
rdd = sc.textFile("/user/cloudera/message.txt")

# Imprime os dados do DataFrame como tabela
rdd.collect()

# Le arquivo "json" e cria o DataFrame
df = sqlContext.read.json("/user/cloudera/pessoas.json")


df.show()

# Imprime Schema do Dataframe
df.printSchema()

# Imprime apenas a coluna nome
df.select("name").show()

# Imprime todos redistros com odeade maior de 23
df.filter(df["age"] > 23).show()

# Imprime agrupamento por idade
df.groupBy("age").count().show()


#save hive nova tabela
df.write.mode("overwrite").format("parquet").option("compression", "zlib").saveAsTable("aula.pessoas")

#save hive tabela existente
#df.write.mode("overwrite").format("parquet").option("compression", "zlib").insertInto(app.pessoas)

# Convert arquivo "json" para parquet
#df.write.parquet("pessoas.parquet")


# Imprime os dados do DataFrame como tabela
df.show()

# Convert arquivo "json" para parquet
#df.write.parquet("pessoas.parquet")

# Le arquivo "parquet" e cria o DataFrame Novo
#dfparq = sqlContext.read.parquet("pessoas.parquet")

# Le o Schema do DataFrame novo
dfparq.printSchema()

# Imprime os dados do DataFrame como tabela
dfparq.show()

df.write.mode("overwrite").format("parquet").option("compression", "zlib").saveAsTable("aula.pessoas")
df.write.mode('append').json("/aula/export/json")
df.write.mode('append').parquet("/aula/export/parquet")

df.rdd.saveAsTextFile("/aula/df_txt")

#read mysql
dataframe_mysql = sqlContext.read.format("jdbc").option("url", "jdbc:mysql://localhost/retail_db").option("driver", "com.mysql.jdbc.Driver").option("dbtable", "categories").option("user", "root").option("password", "cloudera").load()
dataframe_mysql.show()



query = "(select * from categories) t1_alias"
df1 = sqlContext.read.format("jdbc").option("url", "jdbc:mysql://localhost/retail_db").option("driver", "com.mysql.jdbc.Driver").option("dbtable", query).option("user", "root").option("password", "cloudera").load()
df1.show()


dataframe_mysql.registerTempTable("categories")
sqlContext.sql("select * from categories").show()


###################################
#SPARK STREAMING
Exercício 1: Dstream - Stateless

pyspark --master local[2]

from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, 10)
lines = ssc.socketTextStream("localhost", 9999)
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
counts.pprint()
ssc.start()
ssc.awaitTermination()


------------------------------------------
Exercício: Dstream - Stateful
pyspark --master local[2]

from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, 10)
ssc.checkpoint("checkpoint")
def updateFunc(new_values, last_sum):
	return sum(new_values) + (last_sum or 0)
lines = ssc.socketTextStream("localhost", 9999)
running_counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).updateStateByKey(updateFunc)
running_counts.pprint()
ssc.start()
ssc.awaitTermination()

-----------------------------------------------------

from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, 10)
lines = ssc.socketTextStream("localhost", 9999)
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
counts.pprint()
counts.saveAsTextFiles('/tmp/ss')
ssc.start()
ssc.awaitTermination()

###########################################
from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import SQLContext
sc = SparkContext()
sqlContext = HiveContext(sc)

print('Le arquivo "json" e cria o DataFrame')
df = sqlContext.read.json("/user/cloudera/pessoas.json")
df.show()

print('Escrevendo no Hive')

df.write.mode("overwrite").format("parquet").option("compression", "zlib").saveAsTable("aula.pessoas")

print('FIM')


#################
sudo -u hdfs hadoop fs -mkdir /user/spark
sudo -u hdfs hadoop fs -mkdir /user/spark/applicationHistory
sudo -u hdfs hadoop fs -chown -R spark:spark /user/spark
sudo -u hdfs hadoop fs -chmod 1777 /user/spark/applicationHistory

sudo service hadoop-yarn-resourcemanager start
sudo service hadoop-yarn-nodemanager start
sudo service hadoop-mapreduce-historyserver start
