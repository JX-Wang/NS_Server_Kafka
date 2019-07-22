# usr/bin/enc python
# encoding:utf-8
"""
for learing kafka_broker
===================
Author @ wangjunxiong
Date @ 2019/7/19
"""
from kafka import KafkaConsumer, KafkaProducer
from time import sleep


class kafka_producer:
    """
    kafka producer
    func -> kafka_producer("ddivide6", "1.1.1.1:9092").pull("msg")
    """
    def __init__(self, topic, server_list):
        self.server_list = server_list
        self.topic = topic
        self.partition = 1

    def push(self, values):
        try:
            producer = KafkaProducer(bootstrap_servers=[self.server_list], max_request_size=104857600)
            # print self.topic
            # print values
            producer.send(topic=self.topic, value="{values}".format(values=values))
            producer.flush()
        except Exception as e:
            print "E kafka_broker producer send data error:", str(e)


class kafka_consumer:
    """
    kafka consumer
    func -> kafka_consumer("ddivide6", "1.1.1.1:9092").push()
    :return generator but not result
    """
    def __init__(self, topic, server_list):
        self.bootstrap_sever = server_list
        self.topic = topic
        self.partition = 1

    def pull(self):
        try:
            consumer = KafkaConsumer(self.topic, bootstrap_servers=[self.bootstrap_sever])  # topic->str brokers->list
        except:
            print "consumer read error"
        for msg in consumer:
            yield msg.topic, msg.value


class kafka_create_topic:
    """The best way for creating topic is using kafka_broker shell but not python shell"""
    def __init__(self):
        pass

    def create(self):
        pass


class clean_topic:
    """the same as kafka create topic"""
    def __init__(self):
        pass

    def clean(self):
        pass


if __name__ == '__main__':
    topic = "ddivide6"
    server = "10.245.146.115:9092"
    msg_content = kafka_consumer(topic=topic, server_list=server).pull()
    while 1:
        try:
            domain = msg_content.next()
            print domain[1]
            print type(domain[1])
            rst = eval(domain[1])
            print type(rst)
            print len(rst["domains"]), rst["domains"]
            print rst["id"]
            # 这里可以将domain存文件后读取文件进行探测
            # 也可以直接调用domain进行探测
            # 存完文件，或者探测完后，通过while循环再次从生成器中读取发来的的数据
        except Exception as e:
            pass  # 没有next表示broker中没有数据，继续监听即可
    # kafka_producer(topic="nsrst1", server_list="10.245.146.139:9092").push(values="###")



