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
    logging.info('\033[32mStart CMP_install.\033[0m')
    # 实例化类，并调用main方法
    ft_install_CMP = Install_CMP()
    ft_install_CMP.main()
    logging.info("\033[32mInstallation of CMP stand-alone version is complete！\033[0m".center(100, "*"))


if __name__ == '__main__':
    main()