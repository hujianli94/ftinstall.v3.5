# -*- coding: utf-8 -*-
import sys
import logging
import logging.config
from module.tools import CMP_Install_tools as Install_CMP


def main():
    log_format = '%(asctime)s [%(levelname)s] Install: %(message)s 【%(funcName)s】 ->(%(pathname)s:%(lineno)d)'
    logging.basicConfig(level=logging.INFO, filename='install.log', format=log_format)
    formatter = logging.Formatter(log_format)
    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)
    handler_console.setFormatter(formatter)
    logging.getLogger().addHandler(handler_console)
    if len(sys.argv) == 2:
        _, ip = sys.argv
        if ip not in Install_CMP.ip:
            print('IP %s error' % ip)
            exit(1)
        logging.info('\033[32mStart CMP_install.\033[0m')
        # 实例化类，并调用main方法
        ft_install_CMP = Install_CMP()
        ft_install_CMP.main()
        logging.info("\033[32mInstallation of CMP stand-alone version is complete！\033[0m".center(100, "*"))
    else:
        logging.error('Args %s error.' % ' '.join(sys.argv[1:]))
        exit(1)


if __name__ == '__main__':
    # if '192.168.25.152' not in get_ip():
    #     subprocess.call('scp {py} 152:/tmp/install.py && ssh 152 python /tmp/install.py 192.168.25.152'.format(py=__file__), shell=True)
    #     subprocess.call('scp {py} 152:/tmp/install.py'.format(py=__file__), shell=True)
    # else:
    #     main()
    main()
