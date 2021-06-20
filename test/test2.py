# -*- coding: utf-8 -*-
from config import redisCli

redisCli.set('a', 'sxs')
print(redisCli.get('a'))