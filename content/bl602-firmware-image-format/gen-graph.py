#!/usr/bin/env python

import os
import re
import csv

TYPE_DEF_REGEX = re.compile(r'(u?int\d+_t)\s*([\w\[\]]+);\s*\/\*!<\s*(.+)\s*\*\/')
port = 1

print('''
digraph {
    graph [pad="0.5", nodesep="0.5", ranksep="0.5"];
    node [shape=plain]
    rankdir=TB;

''')
# 
# Print the SPI_Flash_Cfg_Type type
print('''
SPI_Flash_Cfg_Type [label=<
<table border="0" cellborder="1" cellspacing="0">
<tr><td><b>Type</b></td><td><b>Name</b></td><td><b>Comment</b></td></tr>''')

with open('SPI_Flash_Cfg_Type.csv', newline='') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)

  for row in reader:
    print('<tr port="{}"><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row[1], row[0], row[1], row[2]))

print('''
</table>>];
 
''')

# Print the Boot_Header_Config type
print('''
Boot_Header_Config [label=<
<table border="0" cellborder="1" cellspacing="0">
<tr><td><b>Type</b></td><td><b>Name</b></td><td><b>Comment</b></td></tr>''')

with open('Boot_Header_Config.csv', newline='') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)

  for row in reader:
    print('<tr><td port="{}">{}</td><td>{}</td><td>{}</td></tr>'.format(row[1], row[0], row[1], row[2]))

print('''
</table>>];

Boot_Header_Config:flashCfg -> SPI_Flash_Cfg_Type;
Boot_Header_Config:clkCfg -> Boot_Clk_Config;
 
''')

# Print the Boot_Clk_Config type
print('''
Boot_Clk_Config [label=<
<table border="0" cellborder="1" cellspacing="0">
<tr><td><b>Type</b></td><td><b>Name</b></td><td><b>Comment</b></td></tr>''')

with open('Boot_Clk_Config.csv', newline='') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)

  for row in reader:
    print('<tr><td port="{}">{}</td><td>{}</td><td>{}</td></tr>'.format(row[1], row[0], row[1], row[2]))

print('''
</table>>];

Boot_Clk_Config:cfg -> Boot_Sys_Clk_Config;
 
''')

# Print the Boot_Sys_Clk_Config type
print('''
Boot_Sys_Clk_Config [label=<
<table border="0" cellborder="1" cellspacing="0">
<tr><td><b>Type</b></td><td><b>Name</b></td><td><b>Comment</b></td></tr>''')

with open('Boot_Sys_Clk_Config.csv', newline='') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)

  for row in reader:
    print('<tr><td>{}</td><td port="{}">{}</td><td>{}</td></tr>'.format(row[0], row[1], row[1], row[2]))

print('''
</table>>];
 
''')
print('}')
