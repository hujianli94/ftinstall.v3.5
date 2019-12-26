# -*- coding: utf-8 -*-
import os
import time
import logging
import shutil
import conf
import re
from conf import get_yml_info
from utility import Base_Tools as tools


class CMP_Install_tools:
    # 类属性，获取ip
    ip = tools.get_ip()
    Mongo_script = os.path.abspath(os.path.dirname(__file__)) + "/conf"
    yml_path = '/etc/ftcloud/compose'  # type: str

    def __init__(self):
        pass

    def _change_Hostname(self):
        tools.run_cmd('hostnamectl set-hostname %s' % '-'.join(self.ip.split('.')))

    def _write_hosts(self):
        Hosts_DNS_info = conf.Host_info
        with open("/etc/hosts", "a") as f:
            f.write(Hosts_DNS_info)

    def _ulimits(self):
        limits = '''\
    * soft noproc 20480
    * hard noproc 20480
    root soft nofile 65535
    root hard nofile 65535
    * soft nofile 65535
    * hard nofile 65535
    '''
        tools.write_file('/etc/security/limits.conf', limits)
        tools.run_cmd('ulimit -n 65535 && ulimit -u 65535')

    def _kernel(self):
        kernel = '''\
    fs.file-max = 20000000
    vm.overcommit_memory = 1
    net.ipv4.tcp_max_tw_buckets = 1000000
    net.ipv4.tcp_fin_timeout = 30
    net.ipv4.tcp_keepalive_time = 300
    net.ipv4.tcp_keepalive_probes = 3
    net.ipv4.tcp_keepalive_intvl = 30
    net.ipv4.tcp_syncookies = 1
    net.ipv4.tcp_tw_reuse = 1
    net.ipv4.tcp_tw_recycle = 1
    net.ipv4.ip_local_port_range = 5000 65000
    net.ipv4.tcp_mem = 786432 1048576 1572864
    net.core.wmem_max = 873200
    net.core.rmem_max = 873200
    net.ipv4.tcp_wmem = 8192 436600 873200
    net.ipv4.tcp_rmem = 32768 436600 873200
    net.core.somaxconn = 10240
    net.core.netdev_max_backlog = 20480
    net.ipv4.tcp_max_syn_backlog = 20480
    net.ipv4.tcp_retries2 = 5
    net.ipv4.conf.lo.arp_ignore = 0
    net.ipv4.conf.lo.arp_announce = 0
    net.ipv4.conf.all.arp_ignore = 0    
    '''
        tools.write_file('/etc/sysctl.conf', kernel)
        tools.run_cmd('sysctl -p >/dev/null 2>&1')

    def _security(self):
        tools.replace('/etc/selinux/config', 'SELINUX=enforcing', 'SELINUX=disabled')
        tools.replace('/etc/selinux/config', 'SELINUX=permissive', 'SELINUX=disabled')
        tools.run_cmd('setenforce 0 >/dev/null 2>&1')

    def _hugepage(self):
        hugepage = '''\
    if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
        echo never > /sys/kernel/mm/transparent_hugepage/enabled
    fi
    if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
        echo never > /sys/kernel/mm/transparent_hugepage/defrag
    fi    
    '''
        tools.write_file('/etc/rc.local', hugepage, mode='a')
        tools.run_cmd('echo never > /sys/kernel/mm/transparent_hugepage/enabled')
        tools.run_cmd('echo never > /sys/kernel/mm/transparent_hugepage/defrag')

    def init_system(self):
        # _ulimits()
        self._change_Hostname()
        self._write_hosts()
        self._kernel()
        self._security()
        self._hugepage()

    def _install_docker(self):
        tools.run3_cmd('yum install -y yum-utils device-mapper-persistent-data lvm2 vim')
        tools.run3_cmd('yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo')
        tools.run3_cmd('yum -y install epel-release')
        tools.run3_cmd('yum -y install python-devel')
        tools.run3_cmd("yum -y install gcc gcc-c++ kernel-devel")
        tools.run3_cmd('yum -y install docker-ce ')
        # _run10_cmd('systemctl start docker && systemctl enable docker')
        docker_conf = '/etc/docker/daemon.json'
        # 配置Daemon.json文件
        docker_conf_cont = '''\
    {"insecure-registries":["%s"]}
    ''' % conf.REGISTRY_URL
        tools.write_file(docker_conf, docker_conf_cont)
        tools.run3_cmd('systemctl start docker && systemctl enable docker')
        # _run10_cmd('systemctl restart docker')
        tools.run3_cmd('docker login %s -u futong -p FuTong+123Me' % conf.REGISTRY_URL)

    def _install_docker_compose(self):
        # 源码安装方式
        # tools.run3_cmd('''curl 'https://bootstrap.pypa.io/get-pip.py' -o /tmp/get-pip.py && python /tmp/get-pip.py &&\
        #  rm -fr /tmp/get-pip.py\
        #  ''')
        # tools.run_cmd(
        #     'sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
        # tools.run_cmd('sudo chmod +x /usr/local/bin/docker-compose')
        # tools.run_cmd("sudo echo 'export PATH=$PATH:/usr/local/bin' > /etc/profile.d/docker-compose.sh")
        # tools.run_cmd("sudo chmod +x /etc/profile.d/docker-compose.sh && source /etc/profile")
        # pip 安装方式
        tools.run_cmd("yum -y install python-pip && pip install --upgrade pip")
        tools.run_cmd('sudo pip install futures')
        tools.run_cmd("sudo pip install --ignore-installed requests")
        tools.run_cmd("pip install docker-compose")

    def install_base(self):
        self._install_docker()
        self._install_docker_compose()

    def pull_image(self, ip):
        all_images = []
        yml_info = get_yml_info(ip)
        for v in yml_info.values():
            # [all_images.append(j) for _, j in v.items() if j and conf.REGISTRY_URL in j]
            [all_images.append(j) for _, j in v.items()]
        # for all_image in all_images:
        #     print(all_image)
        # # [_run10_cmd('docker rmi %s' % i) for i in all_images]
        tools.mulit_run(tools.run3_cmd, len(all_images), ['docker pull %s' % i for i in set(all_images)])

    def _generate_yml(self, ip, path):
        yml_info = get_yml_info(ip)
        yml = {}
        for tmpl in [i for i in os.listdir('template')]:
            with open('template/' + tmpl) as f:
                r = f.read()
                yml[tmpl] = r.format(**yml_info[tmpl]) if tmpl in yml_info else r

        tools.mkdirs(path)
        # 将template/下的的文件写入到path下
        for yml_path, content in yml.items():
            tools.write_file(path + '/%s' % yml_path, content)

    def create_config_dir(self):
        # 生成mongodb-keyfile
        tools.run_cmd("openssl rand -base64 756 > ./conf/mongo/mongodb-keyfile")

        Create_dirs = {"Base-Server": {"Mysql": [conf.mysql_data, conf.mysql_log],
                                       "Rabbitmq": [conf.rabbitmnq_data, conf.rabbitmnq_conf, conf.rabbitmnq_log],
                                       "Redis": [conf.radis_data, conf.redis_conf, conf.redis_log],
                                       "Consul": [conf.consul_data, conf.consul_conf, conf.consul_log],
                                       "Mongo": [conf.mongo_data, conf.mongo_conf,
                                                 conf.mongo1_conf, conf.mongo2_conf,
                                                 conf.mongo3_conf,
                                                 conf.mongo1_keyfile, conf.mongo2_keyfile,
                                                 conf.mongo3_keyfile]},
                       "CMDB-Server": {
                           "CMDB": [conf.cmdb_event_log, conf.cmdb_model_log,
                                    conf.cmdb_resource_log,
                                    conf.cmdb_scene_log]},
                       "Monitor-Server": {"Jk_dir": [conf.prometheus_conf]},

                       "YW-Server": {"YW-server_dir": [conf.yw, conf.yw_monitor_agent,
                                                       conf.futong_cm_monitor, conf.events_agent_data,
                                                       conf.localtime_dir]},
                       "YunY-Server": {"YunY-Server_dir": [conf.YunY_log + "futong-cm-admin-manage",
                                                           conf.YunY_log + "futong-cm-admin-workflow",
                                                           conf.YunY_log + "futong-cm-mq-server",
                                                           conf.YunY_log + "futong-cm-operation-main"]},
                       "ZZ-management": {"ZZ-management_dir": [conf.futong_cm_zuul_log,
                                                               conf.futong_cm_sso_log,
                                                               conf.futong_cm_ucenter_log,
                                                               conf.Resource_management_log + "futong-cm-xxlJob",
                                                               conf.Resource_management_log + "futong-cm-resource-aggregation",
                                                               conf.Resource_management_log + "futong-cm-resource-compute",
                                                               conf.Resource_management_log + "futong-cm-resource-elastic",
                                                               conf.Resource_management_log + "futong-cm-resource-esi",
                                                               conf.Resource_management_log + "futong-cm-resource-network",
                                                               conf.Resource_management_log + "futong-cm-resource-rds",
                                                               conf.Resource_management_log + "futong-cm-resource-nat"
                                                               ]},
                       "Nginx": {"Nginx_dir": [conf.nginx_conf, conf.nginx_log, conf.nginx_html]},

                       }

        # 创建目录
        for Create_dir, dirs in Create_dirs.items():
            print("")
            print("-" * 60)
            print("Start creating {} corresponding directories".format(Create_dir))
            for dir_name, dir in dirs.items():
                for i in dir:
                    tools.mkdirs(i, 999)
                    print("Service name {} create directory {}".format(dir_name, i))

    def copy_config_file(self):
        for root, dirs, files in os.walk("../conf"):
            for file in files:
                dirname = os.path.join(root, file).replace("\\", "/").split("/")[2]
                filename = os.path.join(root, file).replace("\\", "/")
                if dirname == "consul":
                    shutil.copy2(filename, conf.consul_conf)
                elif dirname == "redis":
                    shutil.copy2(filename, conf.redis_conf)
                elif dirname == "rabbitmq":
                    shutil.copy2(filename, conf.rabbitmnq_conf)
                elif dirname == "mongo":
                    if filename.split('/')[-1] == "mongo1.conf":
                        shutil.copy2(filename, conf.mongo1_conf)
                    elif filename.split('/')[-1] == "mongo2.conf":
                        shutil.copy2(filename, conf.mongo2_conf)
                    elif filename.split('/')[-1] == "mongo3.conf":
                        shutil.copy2(filename, conf.mongo3_conf)
                    elif filename.split('/')[-1] == "mongodb-keyfile":
                        mongo_key_name = filename.split('/')[-1]
                        config_list = ["/etc/mongodb/mongo{0}/keyfile".format(i) for i in range(1, 4)]
                        for mongo_key in config_list:
                            shutil.copy2(filename, mongo_key)
                            tools.run_cmd("chown 999 {}".format(mongo_key + "/" + str(mongo_key_name)))
                            tools.run_cmd("chomod 600 {}".format(mongo_key + "/" + str(mongo_key_name)))
                elif dirname == "prometheus":
                    shutil.copy2(filename, conf.prometheus_conf)

    def __Modify_mysql_config(self, filename, one_line_info, old_str, new_str):
        '''
        修改my.cnf文件内容
        '''
        info = ""
        flag = 0
        with open(filename) as f:
            for i in f:
                if i.strip() == one_line_info:
                    i = i.replace(old_str, new_str)
                    info += i
                    flag = 1
                else:
                    info += i

            if flag == 1:
                info += "lower_case_table_names = 1"
            else:
                info += "lower_case_table_names = 1\ndefault-character-set = utf8 "

        with open(filename, "w") as f_w:
            f_w.write(info)

    def check_yml_and_config_Mysql(self, ip):
        '''
        这一步很关键，将yml文件image进行格式化转换，转换为字典的值，就能下载了
        :param ip:  ip
        :return:
        '''
        self._generate_yml(ip, self.yml_path)
        Path_name = self.yml_path + "/" + "00.mysql.yml"
        logging.info("***开始启动mysql容器，复制mysql目录到宿主机..，docker-compose启动测试***")
        result = tools.run3_cmd("sudo docker-compose -f %s up -d" % Path_name)
        tools.YcCheck(result, "启动mysql-test失败..........")
        mysql_docker_id = tools.exec_cmd("docker ps |grep mariadb|awk '{print $1}'")
        # print(mysql_docker_id)
        copy_docker_file = tools.run_cmd("docker cp %s:/etc/mysql /etc/" % mysql_docker_id[1])
        tools.YcCheck(copy_docker_file, "拷贝mysql容器/etc/mysql目录到宿主机失败......")
        mysql_file = "/etc/mysql/my.cnf"
        mariadb_file = "/etc/mysql/mariadb.cnf"
        # 修改my.cnf文件内容
        self.__Modify_mysql_config(mysql_file, "#default-character-set = utf8", "#", "")
        self.__Modify_mysql_config(mariadb_file, "#default-character-set = utf8", "#", "")
        # 关闭mysql服务
        close_mysql = tools.run_cmd("docker-compose -f %s down" % Path_name)
        tools.YcCheck(close_mysql, "docker-compose -f %s down fail....." % Path_name)

    def operate_base_service(self, status=True):
        '''
        启动基础镜像服务，为下面的rabbit和mongo提供环境.
        status=True 启动。
        status=False 关闭
        :return:
        '''
        base_file = self.yml_path + "/" + "01.base-server.yml"
        if status == True:
            result = tools.run_cmd("docker-compose -f %s up -d" % base_file)
            tools.YcCheck(result, "启动docker-base镜像失败.................")
            return result
        elif status == False:
            result = tools.run_cmd("docker-compose -f %s down" % base_file)
            tools.YcCheck(result, "关闭docker-base镜像失败.................")
            return result

    def rabbit_vhost(self):
        # 重复20次等待rabbitmq的启动间隔，超时就退出
        MAX_Second = 20
        n = 0
        # 获取base服务开启状态，如果base开启了，则开始初始化rabbitmq
        start_base_code = self.operate_base_service()
        if start_base_code == 0:
            print(
                "\033[32m ----------------------------开始初始化rabbitmq_vhost --------------------------------------------\033[0m")
            rabbmq_ids = tools.exec_cmd("docker ps | grep rabbitmq:3.7.17-management|awk '{print $1}'")
            rabbmq_id = rabbmq_ids[1] if rabbmq_ids[0] == 0 else None
            while (n <= MAX_Second):
                rst = tools.run_cmd("docker exec -it {} rabbitmqctl status > ./rabbitmq_status.txt".format(rabbmq_id))
                with open("./rabbitmq_status.txt") as f:
                    s = f.readlines()
                    pid_info = s[1].strip("[").strip("{").split(",")[0]
                    if pid_info == "pid":
                        print("\033[32m *********rabbitmq 容器服务启动成功.***************\033[0m")
                        tools.run3_cmd("docker exec -it %s rabbitmqctl add_vhost /" % rabbmq_id)
                        tools.run3_cmd("docker exec -it %s rabbitmqctl add_vhost /resource" % rabbmq_id)
                        tools.run3_cmd("docker exec -it %s rabbitmqctl add_vhost resource" % rabbmq_id)
                        tools.run3_cmd(
                            "docker exec -it %s rabbitmqctl set_permissions -p / user '.*' '.*' '.*'" % rabbmq_id)
                        tools.run3_cmd(
                            "docker exec -it %s rabbitmqctl set_permissions -p /resource user '.*' '.*' '.*'" % rabbmq_id)
                        result = tools.run3_cmd(
                            "docker exec -it %s rabbitmqctl set_permissions -p resource user '.*' '.*' '.*'" % rabbmq_id)
                        return result
                        break
                    else:
                        print("\033[33m ******** rabbitmq docker 服务器启动中 **************** \033[0m")
                        n += 1

    def mongo_init(self):
        # 获取rabbitmq服务初始化状态，如果初始化完毕，则开始配置mongo集群
        init_rabbit_code = self.rabbit_vhost()
        if init_rabbit_code == 0:
            mongo_master = "mongo1"
            tools.run_cmd("chmod 755 %s/%s" % (self.Mongo_script, "mongo_init.sh"))
            tools.run_cmd("docker cp %s/%s %s:/" % (self.Mongo_script, "mongo_init.sh", mongo_master))
            result = tools.run_cmd("docker exec -i %s /bin/bash /mongo_init.sh" % mongo_master)
            tools.YcCheck(result, "***配置 mongo.sh 集群失败****")
            # 去掉mongo集群中的注释
            for root, _, files in os.walk("/etc/mongodb"):
                for file in files:
                    if file == "mongodb-keyfile" or file[-4:] == "_bak":
                        continue
                    filename = os.path.join(root, file)
                    old_info = ""
                    sub_info = ""
                    with open(filename) as fr:
                        for i in fr:
                            line_head = i.rstrip()
                            old_info += line_head + "\n"
                            if re.match("^#", line_head):
                                if re.match("#security:", line_head):
                                    line1 = line_head.replace("#security:", "security:")
                                    sub_info += line1 + "\n"
                                elif re.match("#  authorization: enabled", line_head):
                                    line2 = line_head.replace("#  authorization: enabled", "  authorization: enabled")
                                    sub_info += line2 + "\n"
                                elif re.match("#  keyFile:", line_head):
                                    line3 = line_head.replace("#  keyFile:", "  keyFile:")
                                    sub_info += line3
                    config_mongo = old_info + sub_info
                    # 备份文件
                    tools.write_file(filename + "_bak", old_info)

                    with open(filename, "w") as fw:
                        fw.write(config_mongo)
            return 0

        else:
            return

    def import_db_sql(self):
        """"
        导入sql到数据库
        """
        # 导入数据库前先检测mongo集群已经初始化完毕
        result_mongo_code = self.mongo_init()
        if result_mongo_code == 0:
            mysql_docker_id = tools.exec_cmd("docker ps | grep mariadb|awk '{print $1}'")
            mysql_docker_id = mysql_docker_id[1] if mysql_docker_id[0] == 0 else None
            # 创建mycat_futong_db数据库
            db_name = "mycat_futong_db"  # type: str
            cmd_result = tools.run_cmd(
                'docker exec -it %s mysql -uroot -phello -e"create database %s default charset=utf8;"' % (
                    mysql_docker_id, db_name))
            tools.YcCheck(cmd_result, "创建数据库失败,,,,,,,,")

            # 创建额外4个数据库
            db_names = ["blueprint", "monitoralter", "resource_arrangement", "scripts_data"]
            for db_name in db_names:
                create_db_result = tools.run_cmd(
                    'docker exec -it %s mysql -uroot -phello -e"create database %s default charset=utf8;"' % (
                        mysql_docker_id, db_name))
                tools.YcCheck(create_db_result, "创建数据库失败,,,,,,,,")
            sql_Structure_name = ""
            sql_info = ""
            for root, _, files in os.walk("./db"):
                for file in files:
                    abs_filename = os.path.abspath(os.path.join(root, file))
                    if file == "mycat_futong_db.sql":
                        sql_Structure_name = abs_filename
                    else:
                        sql_info = abs_filename
            # 先导入表结构
            cmd = tools.run_cmd("docker cp %s %s:/home/" % (sql_Structure_name, mysql_docker_id))
            cmd = tools.run_cmd("docker cp %s %s:/home/" % (sql_info, mysql_docker_id))
            tools.YcCheck(cmd, "数据传输入异常，请检查....")
            cmd = tools.run_cmd(
                'docker exec -it %s mysql -uroot -phello %s -e"source /home/%s;"' % (
                    mysql_docker_id, db_name, sql_Structure_name.split('/')[4]))
            tools.YcCheck(cmd, "导入表结构异常,请检查.......")

            # 再导入表初始化数据
            cmd = tools.run_cmd(
                'docker exec -it %s mysql -uroot -phello %s -e"source /home/%s;"' % (
                    mysql_docker_id, db_name, sql_info.split('/')[4]))
            tools.YcCheck(cmd, "导入表结构异常,请检查.......")
            print(
                "\033[32m ---------------------------------------------- 导入数据库完毕 ------------------------------------------\033[0m")
        else:
            raise Exception("导入数据库失败")

    def __command_server(self, status=None, reverse=False):
        """
        :param status:  status == True and reverse == False:  正序开启服务
                        status == False and reverse == True:  倒序关闭服务
        :param reverse:  默认正序
        :return:
        """
        Ordered_list = {}
        for service in os.listdir(self.yml_path):
            Ordered_list[service.split('.')[0][1]] = service
        # 默认正序
        new_dicts = (sorted(Ordered_list.items(), key=lambda item: item[0], reverse=reverse))
        if status == None:
            logging.info(" Check docker status...........")
            tools.run_cmd("docker ps -a")

        elif status == True and reverse == False:
            for server in new_dicts:
                service = server[1]
                # 开启服务,尝试开启2次
                logging.info('Start service: %s' % service[:-4])
                # print(service)
                tools.run_cmd('docker-compose -f %s/%s up -d' % (self.yml_path, service), retry=2)
                time.sleep(1.5)

        elif status == False and reverse == True:
            for server in new_dicts:
                service = server[1]
                # 关闭服务，尝试关闭2次
                logging.info('Stop service: %s' % service[:-4])
                tools.run_cmd("source /etc/profile && docker-compose -f %s/%s down" % (self.yml_path, service), retry=2)
                time.sleep(1.5)

    def start_all_server(self):
        """ 启动服务，正序执行yaml文件，reverse=False，正序"""
        self.__command_server(status=True, reverse=False)

    def stop_all_server(self, reverse=True):
        """ 停止服务，倒顺序执行yaml文件，reverse=True，倒序"""
        self.__command_server(status=False, reverse=True)

    def restart_all_server(self):
        self.stop_all_server()
        self.start_all_server()

    def __open_ports(self):
        result = os.system('yum -y install firewalld && service firewalld restart')
        if result == 0:
            logging.info("******开启firewall防火墙的端口***********")
            [tools.run_cmd('firewall-cmd --zone=public --add-port=%s/tcp --permanent' % str(i)) for i in
             set(conf.TCP_PORTS.split())]
            [tools.run_cmd('firewall-cmd --zone=public --add-port=%s/udp --permanent' % str(i)) for i in
             set(conf.UDP_PORTS.split())]
            tools.run_cmd('firewall-cmd --reload')

    def open_port(self):
        self.__open_ports()

    def start_file_server(self):
        try:
            result = tools.run3_cmd(
                "docker run -d --network=host --name storage -e TRACKER_SERVER=IP:22122 -v /var/fdfs/storage:/var/fdfs --privileged=true -e GROUP_NAME=group1 delron/fastdfs storage")
            if result:
                logging.info("start storage server successful.....")
        except:
            pass

    def main(self):
        ######## 初始化############################
        # self.init_system()
        # self.install_base()
        # self.pull_image(self.ip)
        self.create_config_dir()
        self.copy_config_file()
        ############服务初始化操作######################################
        self.check_yml_and_config_Mysql(self.ip)
        self.operate_base_service()
        self.import_db_sql()
        self.operate_base_service(status=False)  # 关闭base镜像
        self.start_all_server()
        self.open_port()
        self.start_file_server()
        # self.stop_all_server()  # 停止所有服务
        # self.restart_all_server()     # 重启所有服务
