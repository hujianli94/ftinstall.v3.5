#!/usr/bin/env python
#-*- coding:utf8 -*-
# auther; 18793
# Date：2019/12/26 10:08
# filename: a.py
import os

script = os.path.abspath(os.path.dirname(__file__))
html_path = os.path.dirname(script) + "/html/"

print(html_path)