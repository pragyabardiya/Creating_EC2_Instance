# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 15:11:49 2018
@author: Pragya
"""

import boto3

""" Creating a Security Group"""
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

import json
from pprint import pprint

with open('D:\Github\script.json') as f:
    data = json.load(f)
pprint(data)

GroupName =data.get('GroupName')
Description =data.get('Description')
ImageId =data.get('ImageId')
InstanceType =data.get('InstanceType')
KeyName =data.get('KeyName')
Key =data.get('Key')
Value =data.get('Value')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

try:
    response = ec2.create_security_group(GroupName=GroupName,
                                         Description=Description,
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 3389,
             'ToPort': 3389,
             'IpRanges': [{'CidrIp': '192.168.1.105/32'}]}
            ])
    print('Ingress Successfully Set %s' % data)
    
except ClientError as e:
    print(e)
    
Group_id=[]
Group_id.append(str(security_group_id))
print Group_id
  
ec2= boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId=ImageId,
    MinCount=1,
    MaxCount=1,
    InstanceType=InstanceType,
    KeyName=KeyName,
    SecurityGroupIds= Group_id)
print instance[0].id
Id= instance[0].id
print(Id)

"""Creating Tags"""
response = ec2.instances.create_tags(
    Tags=[
        {
            "Key": "Key",
            "Value": "Value"
        }
    ]
)




