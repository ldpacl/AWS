### Create a VPC:
```aws ec2 create-vpc --cidr-block <vpc_cidr_block> --instance-tenancy default --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=demoVPC}]'```

### Create a public subnet:
```aws ec2 create-subnet --vpc-id <vpc_id> --cidr-block <public_subnet_cidr_block> --availability-zone <availability_zone> --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PublicSubnet}]'```

### Create a private subnet:
```aws ec2 create-subnet --vpc-id <vpc_id> --cidr-block <private_subnet_cidr_block> --availability-zone <availability_zone> --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=PrivateSubnet}]'```

### Create an internet gateway:
```aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=demoIGW}]'```

### Attach the internet gateway to the VPC:
```aws ec2 attach-internet-gateway --internet-gateway-id <igw_id> --vpc-id <vpc_id>```

### Create NAT gateway:
```aws ec2 create-nat-gateway --allocation-id <eip_allocation_id> --subnet-id <public_subnet_id>```

### Create a public route table:
```aws ec2 create-route-table --vpc-id <vpc_id> --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=PublicRouteTable}]'```

### Create a private route table:
```aws ec2 create-route-table --vpc-id <vpc_id> --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=PrivateRouteTable}]'```

### Create a route in the public route table:
```aws ec2 create-route --route-table-id <public_route_table_id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw_id>```

### Associate the public route table with the public subnet:
```aws ec2 associate-route-table --route-table-id <public_route_table_id> --subnet-id <public_subnet_id>```

### Create a route in the private route table:
```aws ec2 create-route --route-table-id <private_route_table_id> --destination-cidr-block 0.0.0.0/0 --nat-gateway-id <nat_gateway_id>```

### Associate the private route table with the private subnet:
```aws ec2 associate-route-table --route-table-id <private_route_table_id> --subnet-id <private_subnet_id>```

### Create a public security group:
```aws ec2 create-security-group --group-name public-sg --description "Public Security Group" --vpc-id <vpc_id>```

### Authorize ingress rules for the public security group:
```aws ec2 authorize-security-group-ingress --group-id <public_sg_id> --protocol tcp --port 80 --cidr 0.0.0.0/0```

```aws ec2 authorize-security-group-ingress --group-id <public_sg_id> --protocol tcp --port 22 --cidr 0.0.0.0/0```

### Create a private security group:
```aws ec2 create-security-group --group-name private-sg --description "Private Security Group" --vpc-id <vpc_id>```

### Authorize ingress rules for the private security group:
```aws ec2 authorize-security-group-ingress --group-id <private_sg_id> --protocol tcp --port 22 --cidr <vpc_cidr_block>```

### Create a Public Server:
```aws ec2 run-instances --cli-input-json file://input1.json```

### Create a Private Server:
```aws ec2 run-instances --cli-input-json file://input2.json```