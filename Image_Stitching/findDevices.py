# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:54:53 2018

@author: Sunny
"""

#!/usr/bin/python
import sys
import usb.core
# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
  sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
  sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')