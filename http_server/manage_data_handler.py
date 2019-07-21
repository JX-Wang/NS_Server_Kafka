# encoding:utf-8
"""
主节点控制功能

2019.7.21
~ 修改部分for循环逻辑错误
~ 修改asyn_fetch返回类型
~
"""
import sys

sys.path.append("..")  # 上级目录加入

import tornado.web
import hashlib
import time
import json
from tornado import gen

# 第三方库
from system_parameter import *
from Logger import Logger
from async_fetch import async_fetch, async_post
from kafka_broker.domain_divide_tools import domain_divide
from kafka_broker.kafka_tools import kafka_producer

logger = Logger(file_path='./query_log/', show_terminal=True)  # 日志配置


class RespDomainResultHandler(tornado.web.RequestHandler):
    """
    根据文件名，服务器返回请求的文件内容
    """

    def get(self, file_name):
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_name)
        with open("./verified_domain_data/" + file_name, "r") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)

        self.finish()  # 记得要finish


class TaskConfirmHandler(tornado.web.RequestHandler):
    """
    接收完成探测请求，以及告知对方服务器完成的任务id和文件的url连接
    """

    def save_file(self, domain_ns, file_name):
        """
        根据文件名称，将数据保存到本地
        """
        path = './verified_domain_data/'
        with open(path + file_name, 'w') as fp:
            fp.write(domain_ns)

    @gen.coroutine
    def post(self):
        """
        接收探测任务完成的post请求，并将结果保存本地文件后，将文件链接地址告知对方服务器
        """
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        file_name = param['file_name']  # 文件名称
        task_id = param['task_id']  # 任务id
        domain_ns = param['domain_ns']  # 域名ns的数据
        task_type = param['task_type']  # 任务类型，sec/query
        self.save_file(domain_ns, file_name)  # 将域名ns数据save

        file_md5 = hashlib.md5(domain_ns.encode("utf-8")).hexdigest()  # 生成md5值
        ip, port = read_server('../system.conf')  # 读取主服务器ip地址
        remote_ip, remote_port = read_remote_ip('../system.conf')  # 远程的IP地址
        remote_url = "http://{ip}:{port}/notify/{task_type}/result_list".format(ip=remote_ip, port=str(remote_port),
                                                                                task_type=task_type)  # 远程访问的地址
        file_url = "http://{ip}:{port}/file/{file_name}".format(ip=ip, port=str(port), file_name=file_name)  # 文件存储url
        post_body = {
            "id": task_id,
            "time": time.time(),
            "file_url": file_url,
            "file_md5": file_md5
        }

        for i in range(3):  # 最多重试3次
            respond = yield async_post(remote_url,
                                       json_data=post_body,
                                       data_type="json")
            if respond[0] == 'True':
                resp_code = respond[1]['code']
                if resp_code == 1:
                    logger.logger.info('对方接收域名dns结果文件成功')
                    break
                else:
                    logger.logger.warning('对方接收域名dns结果文件失败，次数：' + str(i + 1) + '/3')
            else:
                exception = respond[1]
                logger.logger.error('向对方发送域名dns结果文件失败:' + str(i + 1) + "/3 " + str(exception))


class RecvDomainRequestHandler(tornado.web.RequestHandler):
    """
    接收来自对方服务器的域名实时/非实时验证请求
    """

    @gen.coroutine
    def post(self, task_type):
        param = self.request.body.decode('utf-8')
        param = json.loads(param)
        try:
            file_url = param['file_url']
            task_id = param['id']
            request_time = param['time']
            file_md5 = param['file_md5']
        except Exception, e:  # 解析失败
            logger.logger.error('请求内容不符合要求：' + str(e))
            self.write({'time': time.time(), 'code': 2})  # 请求内容不符合要求
            self.finish()
            return

        domain_data = yield async_fetch(file_url, "text")
        if domain_data[0] == "False":
            exception = str(domain_data[1])
            logger.logger.error('获取要探测的域名失败：' + exception)
            self.write({'time': request_time, 'code': 2})  # 获取失败
            self.finish()
            return

        domain_data = domain_data[1]  # !

        domain_md5 = hashlib.md5(domain_data.encode("utf-8")).hexdigest()  # 数据自身的md5值

        # 校验数据是否一致
        if domain_md5 == file_md5:
            if task_type in ('sec', 'query'):
                self.write({'time': request_time, 'code': 1})  # 校验一致
                self.finish()
            else:
                logger.logger.error('错误的查询类型：' + str(task_type))
                self.write({'time': request_time, 'code': 2})
                self.finish()
                return
        else:
            logger.logger.error('域名数据校验不一致')
            self.write({'time': request_time, 'code': 2})  # 校验不一致
            self.finish()
            return

        original_file_name = file_url.split('/')[-1]  # 远程文件的名称
        local_file_name = original_file_name + '_' + task_type + '_' + str(task_id)  # 保存到本地的文件名称
        with open("./unverified_domain_data/" + local_file_name, "w") as f:  # 将要验证的域名数据保存到本地
            f.writelines(domain_data)

        if task_type == 'sec':
            periodic_domain_request(domain_data, task_id, local_file_name)  # 执行定时查询节点
        elif task_type == 'query':
            # query_domain_request(domain_data, task_id, local_file_name)  # post 传输数据 执行实时查询节点
            query_domain_request_kafka(domain_data, task_id)  # kafka 传输数据

# @gen.coroutine
# def query_domain_request(domains, task_id, file_name):
#     """
#     将需要实时查询的域名传递给实时查询http_client_realtime
#     """
#     query_ip, port = read_client_realtime('../system.conf')  # 获取实时探测点的ip和端口
#     url = 'http://' + query_ip + ':' + str(port) + '/domain_ns_realtime/'
#     request_data = {
#         'domains': domains,
#         'id': task_id,
#         'file_name': file_name
#     }
#
#     for i in range(3):
#         respond = yield async_post(url, json_data=request_data, data_type="str")
#         if respond[0] == 'True':
#             if respond[1] == 'OK':  # Attention
#                 break
#         else:
#             excpetion = respond[1]
#         logger.logger.error('向实时查询节点发送域名数据失败%s/3' % str(i))


@gen.coroutine
def query_domain_request_kafka(domain_data, task_id):
    """
    :param domain_data:
    :param task_id:
    :param local_file_name:
    :return Null
    :该方法通过kafka将数据拆分后传输到broker中
    """
    server = "10.245.146.115:9092"
    topics = ["ddivide6", "ddivide7", "ddivide8"]
    domains = domain_divide(blocks=3, id=task_id, type="query").bomb(value=domain_data)
    kafka_producer(topic=topics[0], server_list=server).push(values=domains[0])
    kafka_producer(topic=topics[1], server_list=server).push(values=domains[1])
    kafka_producer(topic=topics[2], server_list=server).push(values=domains[2])


@gen.coroutine
def periodic_domain_request(domains, task_id, file_name):
    """
    将需要实时查询的域名传递给定时查询http_client_sec
    """
    periodic_ip, port = read_client_periodic('../system.conf')  # 获取ip地址和端口号
    url = 'http://' + periodic_ip + ':' + str(port) + '/domain_ns_periodic/'
    request_data = {
        'domains': domains,
        'id': task_id,
        'file_name': file_name
    }

    for i in range(3):
        respond = yield async_post(url, json_data=request_data, data_type="str")
        if respond[0] == 'True':
            if respond[1] == 'OK':
                break
        else:
            excpetion = respond[1]
        logger.logger.error('向定时查询节点发送域名数据失败%s/3' % str(i))


if __name__ == '__main__':
    print 1
    local_file_name = "domains"
    with open(local_file_name, 'r') as f:
        domain = f.readlines()
        domain = ['1.com', '1.com', '1.com', '2.com', '2.com', '2.com', '3.com', '3.com', '3.com']
        query_domain_request_kafka(domain_data=domain, task_id=1)
    print "done"