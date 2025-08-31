import time
import boto3

region= input("Enter the region: ")
vpcCidr= input("Enter the VPC CIDR: ")
publicSubnetCidr= input("Enter the Public Subnet CIDR: ")
privateSubnetCidr= input("Enter the Private Subnet CIDR: ")
keyPairName= input("Enter the Key Pair Name: ")
amiId= input("Enter the AMI ID: ")

ec2client=boto3.client('ec2')

try:
    vpcresponse = ec2client.create_vpc(
        CidrBlock=vpcCidr,
        InstanceTenancy='default',
        TagSpecifications=[
            {
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'demoVPC'
                    },
                ]
            },
        ]
    )
    print("VPC created")

    vpc_id = vpcresponse['Vpc']['VpcId']

    public_subnet_response = ec2client.create_subnet(
        AvailabilityZone=region+'a',
        CidrBlock=publicSubnetCidr,
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Public Subnet'
                    },
                ]
            },
        ]
    )
    print("Public Subnet created")

    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    private_subnet_response = ec2client.create_subnet(
        AvailabilityZone=region+'b',
        CidrBlock=privateSubnetCidr,
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Private Subnet'
                    },
                ]
            },
        ]
    )
    print("Private Subnet created")

    private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    igw_response = ec2client.create_internet_gateway(
        TagSpecifications=[
            {
                'ResourceType': 'internet-gateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'demoIGW'
                    },
                ]
            },
        ]
    )
    print("Internet Gateway created")

    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    attach_igw_response = ec2client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )

    eip_response = ec2client.allocate_address(Domain='vpc')
    allocation_id = eip_response['AllocationId']

    nat_response = ec2client.create_nat_gateway(
        AllocationId=allocation_id,
        SubnetId=public_subnet_id
    )
    print("NAT Gateway created")

    nat_id = nat_response['NatGateway']['NatGatewayId']

    while True:
        nat_gateway = ec2client.describe_nat_gateways(
            NatGatewayIds=[nat_id]
        )
        state= nat_gateway['NatGateways'][0]['State']
        if state == 'available':
            break
        time.sleep(10)

    public_route_table_response = ec2client.create_route_table(
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Public Route Table'
                    },
                ]
            },
        ]
    )
    print("Public Route Table created")

    public_route_table_id = public_route_table_response['RouteTable']['RouteTableId']

    private_route_table_response = ec2client.create_route_table(
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Private Route Table'
                    },
                ]
            },
        ]
    )
    print("Private Route Table created")

    private_route_table_id = private_route_table_response['RouteTable']['RouteTableId']

    ec2client.create_route(
        RouteTableId=public_route_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )

    ec2client.associate_route_table(
        RouteTableId=public_route_table_id,
        SubnetId=public_subnet_id
    )

    ec2client.create_route(
        RouteTableId=private_route_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        NatGatewayId=nat_id
    )

    ec2client.associate_route_table(
        RouteTableId=private_route_table_id,
        SubnetId=private_subnet_id
    )

    public_ingress_rules = [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': '0.0.0.0/0'},
        {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'CidrIp': '0.0.0.0/0'}
    ]

    public_sg_response = ec2client.create_security_group(
        Description='Allow SSH and HTTP',
        VpcId=vpc_id,
        GroupName='PublicSG',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Public Security Group'
                    },
                ]
            },
        ]
    )

    public_sg_id = public_sg_response['GroupId']

    for ingress_rule in public_ingress_rules:
        ec2client.authorize_security_group_ingress(
            GroupId=public_sg_id,
            IpPermissions=[
                {'IpProtocol': ingress_rule['IpProtocol'],
                'FromPort': ingress_rule['FromPort'],
                'ToPort': ingress_rule['ToPort'],
                'IpRanges': [{'CidrIp': ingress_rule['CidrIp']}]}
            ]
        )
    print("Public Security Group created")

    private_ingress_rules = [
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'CidrIp': publicSubnetCidr},
    ]

    private_sg_response = ec2client.create_security_group(
        Description='Allow SSH from Public SG',
        VpcId=vpc_id,
        GroupName='PrivateSG',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Private Security Group'
                    },
                ]
            },
        ]
    )

    private_sg_id = private_sg_response['GroupId']

    for ingress_rule in private_ingress_rules:
        ec2client.authorize_security_group_ingress(
            GroupId=private_sg_id,
            IpPermissions=[
                {'IpProtocol': ingress_rule['IpProtocol'],
                'FromPort': ingress_rule['FromPort'],
                'ToPort': ingress_rule['ToPort'],
                'IpRanges': [{'CidrIp': ingress_rule['CidrIp']}]}
            ]
        )
    print("Private Security Group created")

    public_server_response = ec2client.run_instances(
        ImageId=amiId,
        InstanceType='t2.micro',
        KeyName=keyPairName,
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'Groups': [public_sg_id],
                'SubnetId': public_subnet_id
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
                        'Value': 'Public Server'
                    },
                ]
            },
        ]
    )
    print("Public Server created")

    private_server_response = ec2client.run_instances(
        ImageId=amiId,
        InstanceType='t2.micro',
        KeyName=keyPairName,
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': False,
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'Groups': [private_sg_id],
                'SubnetId': private_subnet_id
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
                        'Value': 'Private Server'
                    },
                ]
            },
        ]
    )
    print("Private Server created")     

except Exception as e:
    print("An error occured: ",e)