#!/usr/bin/env python

from __future__ import unicode_literals

from socket import getfqdn
from socket import gethostname
import sys
from urllib import urlopen

import json
import urllib2
import os
import base64
import ssl
from os import environ


INSTANCE_METADATA_URL = 'http://169.254.169.254/latest/meta-data/'


def get_metadata(key, url=INSTANCE_METADATA_URL):
    return urlopen(url + key).read()


def postEventinChat(hostname, privateIp, publicIp, hostPublicDns, hostPrivateDns):
    data = {
        'hostname': hostname,
        'publicIp': publicIp,
        'privateIp': privateIp,
        'publicDns': hostPublicDns,
        'privateDns': hostPrivateDns
    }
    url = os.environ.get('CHAT_WEBHOOK')

    if not url:
        print "CHAT_WEBHOOK env varibale not defined. skipping chat post"
    else:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))


def notify():

    public_ip = get_metadata(key='public-ipv4')
    private_ip = get_metadata(key='local-ipv4')
    public_hostname = get_metadata(key='public_hostname')
    local_hostname = get_metadata(key='public_hostname')

    hostFqn = gethostname()


    postEventinChat(hostname=hostFqn, publicIp=public_ip, privateIp=private_ip,
                    hostPublicDns=public_hostname, hostPrivateDns=local_hostname)


def getConsulContent(contentPath,contentFile,filePermissions):

    if "CONSUL_CONFIG_URL" in os.environ and "CONSUL_CONFIG_TOKEN" in os.environ:
        cfgFile = contentFile or 'app.env'
        url = os.getenv('CONSUL_CONFIG_URL') + '/'+contentPath
        headers = {
            'Content-Type': "application/json",
            'X-Consul-Token': os.getenv('CONSUL_CONFIG_TOKEN')
        }
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            cfgData = response.read()
            print cfgData
            consulResponseJson = json.loads(cfgData)
            print consulResponseJson[0]
            if len(consulResponseJson) > 0:
                cfgValue = consulResponseJson[0]['Value']
                decodedCfg = base64.b64decode(cfgValue).decode('utf-8')
                print('Writing config to file:', cfgFile)
                f = open(cfgFile, 'w')
                f.write(decodedCfg)
                f.close()
                os.chmod(cfgFile, filePermissions)

            else:
                print('Inavlid response. Json response is empty', response.text)

        except urllib2.URLError as e:
            print('Error: Reading config', url)
            print e.reason
    else:
        print('Config not set')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Invalid run arguments, usage vmtools.py <option> <args>')
    else:
        runoption = sys.argv[1]
       
        if runoption == 'chatnotify':
            notify()
        elif runoption == 'getcontent' : 
            if len(sys.argv) < 3:
                print('Invalid arguments, usage vmtools.py getcontent <configpath-in-consul>')
            else:
                contentPath=sys.argv[2]

                if len(sys.argv) > 3:
                    contentFile=sys.argv[3]
                else:
                    contentFile=os.path.basename(contentPath)

                if len(sys.argv) > 4:
                    filePermissions=int(sys.argv[4]) 
                elif '.sh' in contentFile:
                    filePermissions=0o755
                else:
                    filePermissions=0o644   

                getConsulContent(contentPath,contentFile,filePermissions)
        else:
           print('Invalid option or incorrect params',runoption)     
           
        sys.exit(0)
