# encoding:utf-8
from kafka_broker.domain_divide_tools import domain_divide
from kafka_broker.kafka_tools import kafka_producer

def query_domain_request_kafka(domain_data, task_id):
    """
        :param domain_data:
        :param task_id:
        :param local_file_name:
        :return Null
        :该方法通过kafka将数据拆分后传输到broker中
        """

    server = "10.245.146.115:9092"
    topics = ["ddivide6", "ddivide7", "ddivide8", "ddivide9"]
    with open(local_file_name, 'r') as f:
        domain = f.readlines()
    domains = domain_divide(blocks=4, id=1, type="query").bomb(value=domain)

    kafka_producer(topic=topics[0], server_list=server).push(values=domains[0])
    kafka_producer(topic=topics[1], server_list=server).push(values=domains[1])
    kafka_producer(topic=topics[2], server_list=server).push(values=domains[2])
    kafka_producer(topic=topics[3], server_list=server).push(values=domains[3])


if __name__ == '__main__':
    local_file_name = "domains"
    with open(local_file_name, 'r') as f:
        domain = f.readlines()
        query_domain_request_kafka(domain_data=domain, task_id=1)
    print "done"