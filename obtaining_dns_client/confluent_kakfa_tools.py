# usr/bin/enc python
# encoding:utf-8
"""
for learing confluent_kafka
===================
Author @ wangjunxiong
Date @ 2019/7/19
"""
"""
zookeeper/kafka IP
["10.245.146.221:9092", "20.245.146.231:9092", "10.245.146.232:9092"]
topics: 
    dnsrst: partitions 5
    posk-pkg: partitions 5
    query-task: partitions 1
    sec-task: partitions 1
    test: partitions 3
"""

from confluent_kafka import Producer, Consumer


class producer(object):
    def __init__(self, topic, server_list):
        self.topic = topic
        self.servers = server_list
        print 1

    # @staticmethod
    def produce_report(self, msg):
        pass

    def push(self, value):
        print 2
        parma = {
            'bootstrap.servers':self.servers
        }
        print parma
        try:
            confluent_producer = Producer(parma)
            print 3
            confluent_producer.produce(topic=self.topic, value="{value}".format(value=value))
            print 4
            confluent_producer.poll(2)  # timeout 10
            print 5
            confluent_producer.flush(2)
            print 6
            print "send done"
        except Exception as e:
            return "E Kafka Producer error -> ", str(e)


class consumer(object):
    def __init__(self, topic, group, server_list):
        self.topic = topic
        if group:
            self.group = str(group)
        else:self.group = None
        self.servers = server_list

    def pull(self):
        parma = {
            'bootstrap.servers':[self.servers],
            'group.id': self.group,
            'default.topic.config': {
                'auto.offset.reset': 'smallest'
            }
        }
        print parma
        # try:
        confluent_consumer = Consumer(parma)
        print 1
        # confluent_consumer.subscribe(topics=[self.topic])
        confluent_consumer.subscribe(topics=["test"])
        messages = confluent_consumer.consume(num_messages=10)

        print messages, type(messages)
        # print messages.value(payload=)

        # except Exception as e:
        #     print "E Kafka Consumer error -> ", str(e)
        #     pass


if __name__ == '__main__':
    # server_lsit = ["10.245.146.221:9092", "20.245.146.231:9092", "10.245.146.232:9092"]
    # msg = consumer(topic="test", group=1, server_list="10.245.146.221:9092").pull()
    # print 1
    # try:
    #     value = msg.next()
    #     print value
    # except Exception as e:
    #     print e
    #     pass


    server_lsit = ["10.245.146.221:9092", "10.245.146.231:9092"]
    p = producer(topic="test", server_list=server_lsit).push(value="xxxx")