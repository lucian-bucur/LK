#!/usr/bin/python

import requests
import json
from subprocess import Popen,PIPE,STDOUT,call

import sys
def dumpx(ax,bx,key='hostname'):
    dx = {}
    for hostx in ax:
        for v_address in bx:
              command="/usr/bin/host" + ' ' + str(hostx) + '| grep ' + str(v_address)
              proc=Popen(command, shell=True, stdout=PIPE, )
              output=proc.communicate()[0]
              if output == '':
                 if key=='hostname':
                    if hostx not in dx.keys(): dx[hostx] = []
                    dx[hostx].append(v_address.strip())
                 if key=='address':
                    if v_address not in dx.keys(): dx[v_address] = []
                    dx[v_address].append(hostx.strip())
    return dx
