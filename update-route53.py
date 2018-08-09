#!/usr/bin/env python

from __future__ import unicode_literals

from socket import getfqdn
from socket import gethostname
import sys
from urllib import urlopen

import json
import urllib2
import os


from boto.route53.connection import Route53Connection


INSTANCE_METADATA_URL = 'http://169.254.169.254/latest/meta-data/'


def get_metadata(key, url=INSTANCE_METADATA_URL):
    return urlopen(url + key).read()


def postEventinChat(hostname, privateIp, publicIp,hostPublicDns,hostPrivateDns) :
	data = {
       		  'hostname':hostname,
		  'publicIp':publicIp,
          	  'privateIp':privateIp,
                  'publicDns':hostPublicDns,
                  'privateDns':hostPrivateDns
		};
        url = os.environ.get('CHAT_WEBHOOK')
	
	if not url:
	  print  "CHAT_WEBHOOK env varibale not defined. skipping chat post"
	else:
	  req = urllib2.Request(url)
 	  req.add_header('Content-Type', 'application/json')
 	  response = urllib2.urlopen(req, json.dumps(data))



def setHostCname(domain,hostname, hostIp):

    hostFqn = hostname+'.'+domain+'.'
    print domain , hostname , hostFqn
    conn = Route53Connection()
    zone = conn.get_hosted_zone_by_name(domain)
    if zone is None:
        raise ValueError('Invalid CNAME: {0}'.format(domain))

    records = conn.get_all_rrsets(hosted_zone_id=zone.Id.split('/')[-1])
    # Add current CNAME
    change = records.add_change(action='UPSERT',
                                name=hostFqn,
                                type='A',
                                ttl=60)
    change.add_value(hostIp)
    records.commit()


def update_dns():
     
     public_ip = get_metadata(key='public-ipv4');
     private_ip = get_metadata(key='local-ipv4');

     hostFqn = gethostname();
     hostname, domain = hostFqn.split('.', 1);
     hostname_corp=hostname+'-corp'
     hostname_corp_fqn = hostname_corp + '.' +domain	
     setHostCname(domain=domain,hostname=hostname,hostIp=public_ip)
     setHostCname(domain=domain,hostname=hostname_corp,hostIp=private_ip)
     postEventinChat(hostname=hostFqn,publicIp=public_ip,privateIp=private_ip,hostPublicDns=hostFqn,hostPrivateDns=hostname_corp_fqn)
 
    
    


# Provide get_hosted_zone_by_name if it doesn't already exist
if not hasattr(Route53Connection, 'get_hosted_zone_by_name'):
    def get_hosted_zone_by_name(self, hosted_zone_name):
        if hosted_zone_name[-1] != '.':
            hosted_zone_name += '.'
        all_hosted_zones = self.get_all_hosted_zones()
        for zone in all_hosted_zones['ListHostedZonesResponse']['HostedZones']:
            #check that they gave us the FQDN for their zone
            if zone['Name'] == hosted_zone_name:
                return self.get_hosted_zone(zone['Id'].split('/')[-1])
    Route53Connection.get_hosted_zone_by_name = get_hosted_zone_by_name

if __name__ == '__main__':
    update_dns()
    sys.exit(0)
