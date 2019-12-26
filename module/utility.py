# -*- coding: utf-8 -*-
import os
import logging
import logging.config
import subprocess


# from functools import partial

class Base_Tools:
    """
    基础工具方法 类
    """

    @staticmethod
    def YcCheck(return_info, info):
        """
        检查命令执行状态
        :param return_info: 命令返回值
        :param info: 异常提示信息
        :return:
        """
        assert return_info == 0, info

    @classmethod
    def write_file(cls, file_name, content, mode='w', u=0, g=0):
        """
        写文件，创建文件
        :param file_name: 目标文件名称
        :param content:  文件写入内容
        :param mode:
        :param u:
        :param g:
        :return:
        """
        path = os.path.dirname(file_name)
        cls.mkdirs(path, u, g)
        if mode == 'a':
            with open(file_name, 'r') as f:
                if f.read().find(content) != -1:
                    return
        with open(file_name, mode) as f:
            f.write(content)

    @staticmethod
    def mkdirs(file_path, u=0, g=0):
        """
        创建目录
        :param file_path: 目标目录名称
        :param u:
        :param g:
        :return:
        """
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            if u != 0 or g != 0:
                os.chown(file_path, u, g)

    @staticmethod
    def mulit_run(func, max_workers, args):
        """
        多线程执行命令
        :param func:  执行函数
        :param max_workers: 最多线程数
        :param args: 可迭代对象
        :return:
        """
        from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
        executor = ThreadPoolExecutor(max_workers=max_workers)
        all_task = [executor.submit(func, i) for i in args]
        wait(all_task, return_when=ALL_COMPLETED)

    @staticmethod
    def run_cmd(cmd, retry=1):
        """
        执行命令，默认执行一次，log提示执行结果
        :param cmd:
        :param retry:
        :return:
        """
        while retry:
            retry -= 1
            exit_code = subprocess.call(cmd, shell=True)
            if exit_code == 0:
                logging.info('\033[32mRUN %s success.\033[0m' % cmd)
                return exit_code
            else:
                if retry == 0:
                    logging.error('\033[31mRUN %s failed.\033[0m' % cmd)
                    return exit_code

    @classmethod
    def run3_cmd(cls, cmd, retry=3):
        """
        重复执行3次命令
        :param cmd: 执行命令
        :param retry: 默认3次
        :return:
        """
        return cls.run_cmd(cmd, retry)

    @staticmethod
    def exec_cmd(cmd):
        """
        执行命令，不输出，返回元祖--元祖内容 （执行状态，执行输出结果，错误结果）
        """
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                shell=True)
        stdout, stderr = proc.communicate()
        return (proc.returncode, str(stdout).strip(), stderr)

    @staticmethod
    def replace(file_name, old, new):
        """
        :param file_name: 打开文件名
        :param old: 替换前字符串
        :param new: 替换后字符串
        :return:
        """
        assert os.path.isfile(file_name), logging.error('%s not file.' % file_name)
        with open(file_name, 'r+') as f:
            _f = f.read().replace(old, new)
            f.seek(0)
            f.write(_f)
            logging.info('Replace %s ok' % file_name)

    @staticmethod
    def get_ip():
        """
        获取本机IP
        :return:
        """
        return subprocess.check_output('''\
        ip ad|grep -o -e 'inet [0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}'|grep -v "127.0.0"|awk '{print $2}'\
        ''', shell=True).split('\n')[0]

