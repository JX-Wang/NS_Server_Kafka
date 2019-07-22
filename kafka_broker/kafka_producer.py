# usr/bin/enc python
# encoing:utf-8
"""
for learing kafka_broker
===================
Author @ wangjunxiong
Date @ 2019/7/19
"""
from kafka import KafkaConsumer, KafkaProducer
from time import sleep


class kafka_producer:
    def __init__(self):
        self.bootstrap_sever = "10.245.146.115:9092"
        self.topic = "ddivide6"

    def push(self, values):
        print "Start"
        try:
            producer = KafkaProducer(bootstrap_servers=[self.bootstrap_sever])  # topic->str brokers->list
        except:
            print "consumer read error"
            return
        # print 1
        try:
            producer.send(topic=self.topic, value="{values}".format(values=d))
            producer.flush()  # Active sending

            # sleep(5)
        except Exception as e:
            print "E Kafka send Error ->", str(e)
            return


if __name__ == '__main__':
    # d = {
    #     "id": 1,
    #     "domains": [1, 2, 3]
    # }
    with open("domains", 'r') as f:
        # d = f.read()
        d = "11111"
        kafka_producer().push(values=d)
    print "done"

