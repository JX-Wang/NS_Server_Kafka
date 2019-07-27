# from confluent_kafka import Consumer, KafkaError
#
# mybroker = "10.245.146.221:9092"
#
# c = Consumer({
#     'bootstrap.servers': mybroker,
#     'group.id': '1',
#     'default.topic.config': {
#     'auto.offset.reset': 'smallest'
#     }
# })
#
# c.subscribe(['test'])
#
# while True:
#     msg = c.poll()
#
#     if msg is None:
#         print "ops"
#         continue
#     if msg.error():
#         if msg.error().code() == KafkaError._PARTITION_EOF:
#             continue
#         else:
#             print(msg.error())
#             break
#
#     print('Received message: {}'.format(msg.value().decode('utf-8')))
#
# c.close()

from confluent_kafka import Producer

p = Producer({'bootstrap.servers': '10.245.146.221:9092'})


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

data = "XXXX"
p.produce('test', data.encode('utf-8'), callback=delivery_report)

p.poll(10)
p.flush()
