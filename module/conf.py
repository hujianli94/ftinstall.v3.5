# -*- coding: utf-8 -*-
import hashlib

# dockhub镜像仓库地址
REGISTRY_URL = '119.254.93.246:15005'

# 对外服务端口号,注意每行后面有个空格。
Y_J_envt_base = "30023 3306 4396 5010 5016 5671 5672 6010 9091 15671 15672 25672 6379 8300-8302 8400 8500 8080 8686 8070 17082 17086 16006 27016 27017 27018 27019 18080 11000 13001 11001 10086 "
Zy_Management = "4822 5010 5011 6000 5012 8066 30000 30010 30011 30012 30013 30014 30015 30017 30018 30019 30020 30021 30022 "
CMDB_Management = "10006 10007 10008 10009 "
Operation_Management = "8080 8686 5016 6010 5013 "
File_Server = "22122 8888 "
ALL_TCP_Port = Y_J_envt_base + Zy_Management + CMDB_Management + Operation_Management + File_Server
UDP_PORTS = "8301 8302 53"

# mysql服务
mysql_data = "/data/mysql/data"
mysql_log = "/var/log/mysql"

# Rabbitmq服务
rabbitmnq_conf = "/etc/rabbitmq"
rabbitmnq_data = "/data/rabbitmq/data"
rabbitmnq_log = "/var/log/rabbitmq"

# radis服务
radis_data = "/data/redis/data"
redis_conf = "/etc/redis"
redis_log = "/var/log/redis"

# consul服务
consul_data = "/data/consul/data"
consul_conf = "/data/consul/config"
consul_log = "/var/log/consulcd"

# mongo服务
mongo_data = "/data/mongodb/mongo/db"
mongo_conf = "/etc/mongodb/mongo/config"
mongo1_conf = "/etc/mongodb/mongo1/config"
mongo2_conf = "/etc/mongodb/mongo2/config"
mongo3_conf = "/etc/mongodb/mongo3/config"
mongo1_keyfile = "/etc/mongodb/mongo1/keyfile"
mongo2_keyfile = "/etc/mongodb/mongo2/keyfile"
mongo3_keyfile = "/etc/mongodb/mongo3/keyfile"

# CMDB服务
cmdb_event_log = "/home/ftcloud/cmdb/cmdb_event/logs"
cmdb_model_log = "/home/ftcloud/cmdb/cmdb_model/logs"
cmdb_resource_log = "/home/ftcloud/cmdb/cmdb_resource/logs"
cmdb_scene_log = "/home/ftcloud/cmdb/cmdb_scene/logs"
prometheus_conf = "/etc/prometheus"

# 运维服务
yw = "/var/log/ftcloud/yw"
yw_monitor_agent = "/var/log/ftcloud/yw/monitor-agent"
futong_cm_monitor = "/var/log/ftcloud/futong-cm-monitor"
events_agent_data = "/data/events-agent/data"
localtime_dir = "/etc/localtime"

# 运营日志目录
YunY_log = "/var/log/ftcloud/yy/"

## 资源管理日志目录
futong_cm_zuul_log = "/var/log/ftcloud/futong-cm-zuul"
futong_cm_sso_log = "/var/log/ftcloud/futong-cm-sso"
futong_cm_ucenter_log = "/var/log/ftcloud/futong-cm-ucenter"
Resource_management_log = "/var/log/ftcloud/zy/"

## nginx服务
nginx_conf = "/etc/nginx"
nginx_log = "/var/log/nginx"
nginx_html = "/usr/share/nginx/html"

## ft配置目录
Ft_DIR = "/etc/ftcloud"

Host_info = '''\
127.0.0.1 mongodb.service.ftcloud
127.0.0.1 rabbitmq.service.ftcloud
127.0.0.1 consul.service.ftcloud
127.0.0.1 mysql.service.ftcloud 
127.0.0.1 redis.service.ftcloud
127.0.0.1 events-service.service.ftcloud
127.0.0.1 events-agent.service.ftcloud
127.0.0.1 cm.fdfs.url
127.0.0.1 fdfs.service.ftcloud
127.0.0.1 futong-cm-admin-workflow.service.ftcloud
127.0.0.1 futong-cm-audit.service.ftcloud
127.0.0.1 cm-mq-server.service.ftcloud
127.0.0.1 cm-admin.service.ftcloud
127.0.0.1 cm-config.service.ftcloud
127.0.0.1 cm-sso.service.ftcloud
127.0.0.1 cm-txlcn.service.ftcloud
127.0.0.1 cm-ucenter.service.ftcloud
127.0.0.1 cm-zuul.service.ftcloud
127.0.0.1 cm-operation.service.ftcloud
127.0.0.1 cm-modeler.service.ftcloud
127.0.0.1 cmdb-model.service.ftcloud
127.0.0.1 cmdb-resource.service.ftcloud
127.0.0.1 cmdb-scene.service.ftcloud
127.0.0.1 cmdb-event.service.ftcloud
127.0.0.1 resource-xxlJob.service.ftcloud
127.0.0.1 resource-aggregationl.service.ftcloud
127.0.0.1 resource-compute.service.ftcloud
127.0.0.1 resource-elastic.service.ftcloud
127.0.0.1 resource-esi.service.ftcloud
127.0.0.1 resource-network.service.ftcloud
127.0.0.1 resource-rds.service.ftcloud
127.0.0.1 resource-guacd.service.ftcloud
127.0.0.1 resource-guacamole.service.ftcloud
127.0.0.1 resource-nat.service.ftcloud
127.0.0.1 resource-elb.service.ftcloud
127.0.0.1 resource-vpn.service.ftcloud
127.0.0.1 resource-cdn.service.ftcloud
127.0.0.1 futong-cm-source-arrangement.service.ftcloud
127.0.0.1 auto-monitor-server.service.ftcloud
127.0.0.1 futong-cm-scripts-manage.service.ftcloud
127.0.0.1 futong-cm-blueprint.service.ftcloud
127.0.0.1 prometheus.service.ftcloud
127.0.0.1 alertmanager.service.ftcloud
127.0.0.1 pushgateway.service.ftcloud
127.0.0.1 cm.consul.url
127.0.0.1 resource-cloudmanager.service.ftcloud
127.0.0.1 futong-cm-resource-virtualization
'''

# Linux内核优化
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

# 文件最大打开数量
limits = '''\
* soft noproc 20480
* hard noproc 20480
root soft nofile 65535
root hard nofile 65535
* soft nofile 65535
* hard nofile 65535
'''

# 开机自启动配置
hugepage = '''\
if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
fi
if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
    echo never > /sys/kernel/mm/transparent_hugepage/defrag
fi    
'''


def get_yml_info(ip):
    manage_ip = ip
    erlang_cookie = hashlib.md5()
    erlang_cookie.update(ip.encode('utf-8'))
    erlang_cookie = erlang_cookie.hexdigest()
    return {
        '00.mysql.yml': {
            'mysql-test': 'mariadb:10.4.7'
        },

        '01.base-server.yml': {
            'mysql': 'mariadb:10.4.7',
            'rabbitmq': 'rabbitmq:3.7.17-management',
            'redis': 'redis:5.0.5',
            'cookie': erlang_cookie,
            'consul': 'consul:1.5.3',
            'mongo': 'mongo:4.2.0',
            'java': 'java:8',
            'mysql-8': 'mysql:8.0.13',
            'mysql-5': 'mysql:5.6.29'
            # 'ip': manage_ip
        },
        '02.java-public.yml': {
            'futong-cm-resource-xxljob': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-xxljob:1.0.0'),
            'futong-cm-config': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-config:1.0.0'),
            'futong-cm-zuul': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-zuul:1.0.0'),
            'futong-cm-sso': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-sso:1.0.0'),
            'futong-cm-ucenter': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-ucenter:1.0.0')
        },
        '03.events-service.yml': {
            'events_agent': '{0}/public/events-agent:v1'.format(REGISTRY_URL),
            'events_service': '{0}/public/events-service:v1'.format(REGISTRY_URL)
        },
        '04.zy-server.yml': {
            'futong-cm-resource-aggregation': '{0}/resource/{1}'.format(REGISTRY_URL,
                                                                        'futong-cm-resource-aggregation:1.0.0'),
            'futong-cm-resource-compute': '{0}/resource/{1}'.format(REGISTRY_URL,
                                                                    'futong-cm-resource-compute:1.0.0'),
            'futong-cm-resource-elastic': '{0}/resource/{1}'.format(REGISTRY_URL,
                                                                    'futong-cm-resource-elastic:1.0.0'),
            'futong-cm-resource-esi': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-resource-esi:1.0.0'),
            'futong-cm-resource-network': '{0}/resource/{1}'.format(REGISTRY_URL,
                                                                    'futong-cm-resource-network:1.0.0'),
            'futong-cm-resource-rds': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-resource-rds:1.0.0'),
            'futong-cm-resource-nat': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-resource-nat:1.0.0'),
            'guacd': '{0}/resource/{1}'.format(REGISTRY_URL, 'guacd:1.0.0'),
            'futong-cm-resource-cm': "{0}/resource/{1}".format(REGISTRY_URL, 'futong-cm-resource-cm:4.7.0'),
            'futong-cm-resource-elb': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-resource-elb:1.0.0'),
            'futong-cm-resource-cdn': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-resource-cdn:1.0.0'),
            'futong-cm-resource-routetable': '{0}/resource/{1}'.format(REGISTRY_URL,
                                                                       'futong-cm-resource-routetable:1.0.0'),
        },

        '05.yy-server.yml': {
            'futong-cm-admin-manage': '{0}/operation/{1}'.format(REGISTRY_URL, 'futong-cm-admin-manage:1.0.0'),
            'futong-cm-admin-workflow': '{0}/operation/{1}'.format(REGISTRY_URL,
                                                                   'futong-cm-admin-workflow:1.0.0'),
            'futong-cm-audit': '{0}/operation/{1}'.format(REGISTRY_URL, 'futong-cm-audit:1.0.0'),
            'futong-cm-mq-server': '{0}/operation/{1}'.format(REGISTRY_URL, 'futong-cm-mq-server:1.0.0'),
            'futong-cm-operation-main': '{0}/operation/{1}'.format(REGISTRY_URL,
                                                                   'futong-cm-operation-main:1.0.0')

        },
        '06.yw-server.yml': {
            'futong-cm-source-arrangement': '{0}/yw/{1}'.format(REGISTRY_URL,
                                                                'futong-cm-source-arrangement:latest'),
            'futong-cm-blueprint': '{0}/yw/{1}'.format(REGISTRY_URL, 'futong-cm-blueprint:latest'),
            'futong-cm-monitor-agent': '{0}/yw/{1}'.format(REGISTRY_URL, 'futong-cm-monitor-agent:latest'),
            'futong-cm-monitor': '{0}/yw/{1}'.format(REGISTRY_URL, 'futong-cm-monitor:latest'),
            'futong-cm-scripts-manage': '{0}/yw/{1}'.format(REGISTRY_URL, 'futong-cm-scripts-manage:latest'),
            'scripts-manage': '{0}/yw/{1}'.format(REGISTRY_URL, "futong-cm-scripts-manage:latest")
        },
        '07.jk-server.yml': {
            'futong-cm-auto-prometheus': 'prom/{0}'.format('prometheus:latest'),
            'futong-cm-auto-alertmanager': 'prom/{}'.format('alertmanager:latest'),
            'futong-cm-auto-pushgateway': 'prom/{0}'.format('pushgateway:latest'),
            'monitor': '{0}/{1}'.format(REGISTRY_URL, 'monitor:latest'),
        },
        '08.cmdb-server.yml': {
            'cmdb_event': '{0}/cmdb/{1}'.format(REGISTRY_URL, 'futong_cmdb_event:latest'),
            'cmdb_model': '{0}/cmdb/{1}'.format(REGISTRY_URL, 'futong_cmdb_model:latest'),
            'cmdb_resource': '{0}/cmdb/{1}'.format(REGISTRY_URL, 'futong_cmdb_resource:latest'),
            'cmdb_scene': '{0}/cmdb/{1}'.format(REGISTRY_URL, 'futong_cmdb_scene:latest')
        },
        '09.nginx.yml': {
            'nginx': '{0}/public/{1}'.format(REGISTRY_URL, 'nginx:1.17.5')
        }

    }
