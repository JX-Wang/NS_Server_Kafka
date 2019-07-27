from confluent_kafka import Consumer, KafkaError
import json


c = Consumer({
    'bootstrap.servers': '10.245.146.221:9092',
    'group.id': '1',
    # 'auto.offset.reset': 'earliest'
})

c.subscribe(['test'])

while True:
    msg = c.poll(10)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
# kafka_consumer = Consumer(
#
#     {
#
#         "api.version.request": True,
#
#         "enable.auto.commit": True,
#
#         "group.id": 1,
#
#         "bootstrap.servers": '10.245.146.221',
#
#         "security.protocol": "ssl",
#
#         "default.topic.config": {"auto.offset.reset": "smallest"}
#
#     }
#
# )
#
# kafka_consumer.subscribe(["test"])
#
# # Now loop on the consumer to read messages
#
# running = True
#
# while running:
#     message = kafka_consumer.poll()
#
#     application_message = json.load(message.value.decode())
#
# kafka_consumer.close()
