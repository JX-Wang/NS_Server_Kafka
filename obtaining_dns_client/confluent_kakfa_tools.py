# usr/bin/enc python
# encoding:utf-8
"""
for learing confluent_kafka
===================
Author @ wangjunxiong
Date @ 2019/7/27
"""
"""
zookeeper/kafka IP
["10.245.146.221:9092", "20.245.146.231:9092", "10.245.146.232:9092"]
topics: 
    dnsrst: partitions 1
    posk-pkg: partitions 1
    query-task: partitions 5
    sec-task: partitions 5
    test: partitions 3
"""

from confluent_kafka import Producer, Consumer


class confluent_kafka_producer(object):
    """
    confluent kafka producer

    .. py:function:: confluent_kafka_producer(topic="test", servers='kafka1:9092, kafka2:9092, kafka3:9092').push(value="test")

    :param str topic
    :param str servers: 'kafka1:9092, kafka2:9092, kafka3:9092'
    :param float timeout: Maximum time to block waiting for events. (Seconds)
    :return None
    """
    def __init__(self, topic, servers, timeout):  # Attention->servers isn't a list !
        self.topic = topic
        self.servers = servers
        self.timeout = timeout
        parma = {
            'bootstrap.servers':self.servers
        }
        self.confluent_producer = Producer(parma)

    def push(self, value):
        """
        :param str value
        :return: None

        .. py:function:: push(value)

        """
        def delivery_report(err, msg):
            if err is not None:
                print('Message delivery failed: {}'.format(err))
                # you can log here
            else:
                print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
                # you can log here
            pass

        try:
            self.confluent_producer.poll(self.timeout)  # timeout
            self.confluent_producer.produce(topic=self.topic, value="{value}".format(value=value), callback=delivery_report)
            self.confluent_producer.flush()
        except Exception as e:
            # you can log here
            return "E Kafka Producer error -> ", str(e)


class confluent_kafka_consumer(object):
    """
    confluent kafka consumer

    .. py -> consumer(topic="test", group=1, servers='kafka1:9092, kafka2:9092, kafka3:9092', timeout=1).pull()

    :param str topic
    :param str servers: 'kafka1:9092, kafka2:9092, kafka3:9092'
    :param float timeout: Maximum time to block waiting for events. (Seconds)
    :param str auto_offset_reset: ...
    :return None
    """
    def __init__(self, topic, group, servers, timeout=0, auto_offset_reset='latest'):  # Attention->servers isn't a list !
        self.topic = topic
        if group:
            self.group = str(group)
        else:self.group = None
        self.servers = servers
        self.timeout = timeout
        self.auto_offset_reset = auto_offset_reset  # or earliest

    def pull(self):
        """
        :param None
        :return: consumer's generator

        .. py:function:: pull()

        """
        parma = {
            'bootstrap.servers': self.servers,
            'group.id': self.group,
            'enable.auto.commit': True,
            'auto.offset.reset': self.auto_offset_reset
        }
        confluent_consumer = ""
        try:
            confluent_consumer = Consumer(parma)
            confluent_consumer.subscribe([self.topic])  # set kafka cluster topic - > list
        except Exception as e:
            # you can log here
            yield "E confluent_consumer error ->", str(e)
        while 1:
            msg = confluent_consumer.poll(self.timeout)  # pull msg
            if msg is None:
                continue
            if msg.error():
                # you can log here
                print("Consumer error: {}".format(msg.error()))
                continue
            # you can log here
            yield msg.topic().decode('utf-8'), msg.value().decode('utf-8'), msg.partition()
            # print('Received message: {}'.format(confluent_consumer.value().decode('utf-8')))


if __name__ == '__main__':
    # pass
    servers = '10.245.146.221:9092,10.245.146.231:9092,10.245.146.232:9092'
    msg = confluent_kafka_consumer(topic="test", group=1, servers=servers, timeout=1, auto_offset_reset='latest').pull()

    while 1:
        try:
            value = msg.next()
            print value
        except Exception as e:
            pass
    # rst -> (u'test', u'eee')


    # servers = '10.245.146.221:9092,10.245.146.231:9092,10.245.146.232:9092'
    # p = confluent_kafka_producer(topic="test", servers=servers, timeout=0)
    # while True:
    #      for data in range(10):
    #          p.push(value=data)
