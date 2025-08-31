import boto3
import time

region1 = input("Enter the region for VPC1: ")
region2 = input("Enter the region for VPC2: ")

vpc1cidr = input("Enter the CIDR block for VPC1: ")
vpc2cidr = input("Enter the CIDR block for VPC2: ")

subnet1cidr = input("Enter the CIDR block for Subnet1: ")
subnet2cidr = input("Enter the CIDR block for Subnet2: ")

imageid1 = input("Enter the AMI ID for Server1: ")
imageid2 = input("Enter the AMI ID for Server2: ")

keypair1 = input("Enter the keypair name for Server1: ")
keypair2 = input("Enter the keypair name for Server2: ")

instance_type1 = input("Enter the instance type for Server1: ")
instance_type2 = input("Enter the instance type for Server2: ")

ec2client=boto3.client('ec2')
ec2client2=boto3.client('ec2', region_name=region2)

try:
    vpcresponse1 = ec2client.create_vpc(
        CidrBlock=vpc1cidr,
        InstanceTenancy='default',
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'VPC1'
                    },
                ]
            },
        ]
    )
    print("VPC1 created successfully")

    vpc1id = vpcresponse1['Vpc']['VpcId']

    vpcresponse2 = ec2client2.create_vpc(
        CidrBlock=vpc2cidr,
        InstanceTenancy='default',
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'VPC2'
                    },
                ]
            },
        ]
    )
    print("VPC2 created successfully")

    vpc2id = vpcresponse2['Vpc']['VpcId']

    vpcpeeringresponse = ec2client.create_vpc_peering_connection(
        PeerVpcId = vpc2id,
        VpcId = vpc1id,
        PeerRegion = region2
    )
    print("VPC peering connection created successfully")

    vpcpeeringid = vpcpeeringresponse['VpcPeeringConnection']['VpcPeeringConnectionId']

    time.sleep(10)

    acceptvpcpeeringresponse = ec2client2.accept_vpc_peering_connection(
        VpcPeeringConnectionId = vpcpeeringid
    )
    print("VPC peering connection accepted successfully")

    subnetresponse1 = ec2client.create_subnet(
        AvailabilityZone=region1+'a',
        CidrBlock=subnet1cidr,
        VpcId=vpc1id,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Subnet1'
                    },
                ]
            },
        ]
    )
    print("Subnet1 created successfully")

    subnet1id = subnetresponse1['Subnet']['SubnetId']

    subnetresponse2 = ec2client2.create_subnet(
        AvailabilityZone=region2+'a',
        CidrBlock=subnet2cidr,
        VpcId=vpc2id,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Subnet2'
                    },
                ]
            },
        ]
    )
    print("Subnet2 created successfully")

    subnet2id = subnetresponse2['Subnet']['SubnetId']

    igwresponse = ec2client.create_internet_gateway(
        TagSpecifications=[
            {
                'ResourceType': 'internet-gateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'IGW'
                    },
                ]
            }
        ]
    )
    print("Internet Gateway created successfully")

    igwid = igwresponse['InternetGateway']['InternetGatewayId']

    attachigwresponse = ec2client.attach_internet_gateway(
        InternetGatewayId = igwid,
        VpcId = vpc1id
    )

    routetable1response = ec2client.create_route_table(
        VpcId = vpc1id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'RouteTable1'
                    },
                ]
            }
        ]
    )
    print("Route Table1 created successfully")

    routetable1id = routetable1response['RouteTable']['RouteTableId']

    routetable2response = ec2client2.create_route_table(
        VpcId=vpc2id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'RouteTable2'
                    },
                ]
            }
        ]
    )
    print("Route Table2 created successfully")

    routetable2id = routetable2response['RouteTable']['RouteTableId']

    ec2client.create_route(
        RouteTableId=routetable1id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igwid
    )

    ec2client.create_route(
        RouteTableId=routetable1id,
        DestinationCidrBlock='10.2.0.0/24',
        VpcPeeringConnectionId=vpcpeeringid
    )

    ec2client.associate_route_table(
        RouteTableId=routetable1id,
        SubnetId=subnet1id
    )

    ec2client2.create_route(
        RouteTableId=routetable2id,
        DestinationCidrBlock='10.1.0.0/24',
        VpcPeeringConnectionId=vpcpeeringid
    )

    ec2client2.associate_route_table(
        RouteTableId=routetable2id,
        SubnetId=subnet2id
    )

    ingress_rule_1 = [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '0.0.0.0/0'},
    ]

    securitygroup1response = ec2client.create_security_group(
        Description='Allow SSH',
        VpcId=vpc1id,
        GroupName='SecurityGroup1',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'SecurityGroup1'
                    },
                ]
            }
        ]
    )

    securitygroup1id = securitygroup1response['GroupId']

    for ingress_rule in ingress_rule_1:
        ec2client.authorize_security_group_ingress(
            GroupId=securitygroup1id,
            IpPermissions=[
                {'IpProtocol': ingress_rule['IpProtocol'],
                'FromPort': ingress_rule['FromPort'],
                'ToPort': ingress_rule['ToPort'],
                'IpRanges': [{'CidrIp': ingress_rule['CidrIp']}]
                }
            ]
        )
    print("Security Group 1 created successfully")

    ingress_rule_2 = [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '10.1.0.0/0'}
    ]

    securitygroup2response = ec2client2.create_security_group(
        Description='Allow SSH',
        VpcId=vpc2id,
        GroupName='SecurityGroup2',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'SecurityGroup2'
                    },
                ]
            }
        ]
    )

    securitygroup2id = securitygroup2response['GroupId']

    for ingress_rule in ingress_rule_2:
        ec2client2.authorize_security_group_ingress(
            GroupId=securitygroup2id,
            IpPermissions=[
                {'IpProtocol': ingress_rule['IpProtocol'],
                'FromPort': ingress_rule['FromPort'],
                'ToPort': ingress_rule['ToPort'],
                'IpRanges': [{'CidrIp': ingress_rule['CidrIp']}]
                }
            ]
        )
    print("Security Group 2 created successfully")

    server1response = ec2client.run_instances(
        ImageId=imageid1,
        InstanceType=instance_type1,
        KeyName=keypair1,
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'SubnetId': subnet1id,
                'Groups': [securitygroup1id]
            }
        ],
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                }
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Server1'
                    },
                ]
            }
        ]
    )
    print("Server1 created successfully")

    server2response = ec2client2.run_instances(
        ImageId=imageid2,
        InstanceType=instance_type2,
        KeyName=keypair2,
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': False,
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'SubnetId': subnet2id,
                'Groups': [securitygroup2id]
            }
        ],
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                }
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Server2'
                    },
                ]
            }
        ]
    )
    print("Server2 created successfully")

except Exception as e:
    print("An error occured: ", e)