# -*- coding: utf-8 -*-
import hashlib

REGISTRY_URL = '119.254.93.246:15005'

TCP_PORTS = "22 3306 4396 5671 5672 15671 15672 27017 27018 27019 25672 6379 8300-8302 8400 8500 17082 17086 16006 8080"
UDP_PORTS = "8301 8302 53"

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
            'futong-cm-resource-xxljob': '{0}/resource/{1}'.format(REGISTRY_URL, 'futong-cm-xxljob:1.0.0'),
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
            'scripts-manage': '{0}/yw/{1}'.format(REGISTRY_URL,"futong-cm-scripts-manage:latest")
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
