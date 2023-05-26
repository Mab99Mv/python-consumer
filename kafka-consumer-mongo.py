# Import some necessary modules
# pip install kafka-python
# pip install pymongo
# pip install "pymongo[srv]"
from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import subprocess



# replace here with your mongodb url 
mongo_uri = 'mongodb+srv://mabelperezgaribay:ZsPXAYRZpjV7kcDf@cluster0.zv22hfc.mongodb.net/?retryWrites=true&w=majority'
client= MongoClient(mongo_uri)


# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# Connect to MongoDB and pizza_data database

try:

    db = client.Cluster0
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

consumer = KafkaConsumer('test',bootstrap_servers=[
     'my-kafka-0.my-kafka-headless.new-mab99mv.svc.cluster.local:9092'
    ])

# Parse received data from Kafka
for msg in consumer:
    record = json.loads(msg.value)
    print(record)
    name = record['name']

    # Create dictionary and ingest data into MongoDB
    try:
       meme_rec = {'name':name }
       print (meme_rec)
       meme_id = db.memes_info.insert_one(meme_rec)
       print("Data inserted with record ids", meme_id)


    except Exception as e:
       print("Could not insert into MongoDB: ", e)
