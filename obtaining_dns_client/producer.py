from confluent_kafka import Producer
p = Producer({'bootstrap.servers': '10.245.146.221:9092,10.245.146.231:9092,10.245.146.232:9092'})
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
some_data_source = ["111111111", "222222222", "3333333", "444444444", "555555555", "66666666"]
while True:
    for data in some_data_source:
        p.poll(0)
        p.produce('test', data.encode('utf-8'), callback=delivery_report)
        p.flush()

