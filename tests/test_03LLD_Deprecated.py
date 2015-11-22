#!/usr/bin/env python

# -*- coding: utf-8 -*-

import unittest

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import protobix

class TestDeprecatedLLD(unittest.TestCase):

    data = {
        'myhost1': {
            'my.zabbix.lld_item1': [
                { 'my.zabbix.ldd_key1': 0,
                  'my.zabbix.ldd_key2': 'lld string' },
                { 'my.zabbix.ldd_key3': 1,
                  'my.zabbix.ldd_key4': 'another lld string' }
            ]
        },
        'myhost2': {
            'my.zabbix.lld_item2': [
                { 'my.zabbix.ldd_key10': 10,
                  'my.zabbix.ldd_key20': 'yet an lld string' },
                { 'my.zabbix.ldd_key30': 2,
                  'my.zabbix.ldd_key40': 'yet another lld string' }
            ]
        }
    }
    data_type = 'lld'

    def setUp(self):
      self.zbx_container = protobix.DataContainer()
      self.zbx_container._items_list = []
      self.zbx_container._config = {
          'server': '127.0.0.1',
          'port': 10051,
          'log_level': 3,
          'log_output': '/tmp/zabbix_agentd.log',
          'dryrun': False,
          'data_type': None,
          'timeout': 3,
      }

    def tearDown(self):
      self.zbx_container._items_list = []
      self.zbx_container._config = {
          'server': '127.0.0.1',
          'port': 10051,
          'log_level': 3,
          'log_output': '/tmp/zabbix_agentd.log',
          'dryrun': False,
          'data_type': None,
          'timeout': 3,
      }
      self.zbx_container = None

    def testBulkAddAndSent(self):
      self.zbx_container.data_type = self.data_type
      self.assertEqual(self.zbx_container.items_list, [])
      self.zbx_container.add(self.data)
      ''' Send data to zabbix '''
      ret = self.zbx_container.send()
      self.assertEqual(self.zbx_container.items_list, [])

    def testZabbixConnectionFails(self):
      self.zbx_container.zbx_port = 10052
      self.zbx_container.data_type = self.data_type
      self.assertEqual(self.zbx_container.items_list, [])
      self.zbx_container.add(self.data)
      ''' Send data to zabbix '''
      with self.assertRaises(IOError):
        ret = self.zbx_container.send()
      self.assertEqual(self.zbx_container.items_list, [])