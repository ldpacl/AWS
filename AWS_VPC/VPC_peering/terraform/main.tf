provider "aws" {
  region = var.vpc-1-region
}

provider "aws" {
  alias = "region-2"
  region = var.vpc-2-region
}

resource "aws_vpc" "vpc-1" {
  cidr_block = var.vpc-1-cidr_block
  tags = {
    Name = "vpc-1"
  }
}

resource "aws_vpc" "vpc-2" {
  provider = aws.region-2
  cidr_block = var.vpc-2-cidr_block
  tags = {
    Name = "vpc-2"
  }
}

resource "aws_subnet" "subnet-1" {
  vpc_id = aws_vpc.vpc-1.id
  cidr_block = var.subnet-1-cidr_block
  availability_zone = var.subnet-1-az
  map_public_ip_on_launch = true

  tags = {
    Name = "subnet-1"
  }
}

resource "aws_subnet" "subnet-2" {
  provider = aws.region-2
  vpc_id = aws_vpc.vpc-2.id
  cidr_block = var.subnet-2-cidr_block
  availability_zone = var.subnet-2-az
  tags = {
    Name = "subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc-1.id
  tags = {
    Name = "igw"
  }
}

resource "aws_route_table" "subnet-1-rt" {
  vpc_id = aws_vpc.vpc-1.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  route {
    cidr_block = "10.2.0.0/16"
    gateway_id = aws_vpc_peering_connection.vpcpeering.id
  }
}

resource "aws_route_table_association" "rta-1" {
  subnet_id = aws_subnet.subnet-1.id
  route_table_id = aws_route_table.subnet-1-rt.id
}

resource "aws_route_table" "subnet2-rt" {
  provider = aws.region-2
  vpc_id = aws_vpc.vpc-2.id

  route {
    cidr_block = "10.1.0.0/16"
    gateway_id = aws_vpc_peering_connection.vpcpeering.id
  }
}

resource "aws_route_table_association" "rta-2" {
  provider = aws.region-2
  subnet_id = aws_subnet.subnet-2.id
  route_table_id = aws_route_table.subnet2-rt.id
}

resource "aws_vpc_peering_connection" "vpcpeering" {
  peer_owner_id = var.account-id
  peer_vpc_id = aws_vpc.vpc-2.id
  vpc_id = aws_vpc.vpc-1.id
  peer_region = var.vpc-2-region
  auto_accept = false

  tags = {
    Name = "vpc1-vpc2"
  }
}

resource "aws_vpc_peering_connection_accepter" "peer" {
  provider = aws.region-2
  vpc_peering_connection_id = aws_vpc_peering_connection.vpcpeering.id
  auto_accept = true
  
  tags = {
    Side = "Accepter"
  }
}

resource "aws_security_group" "peering-sg-1" {
  name = "peering-sg"
  vpc_id = aws_vpc.vpc-1.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "peering-sg1"
  }
}

resource "aws_security_group" "peering-sg-2" {
  provider = aws.region-2
  name = "peering-sg"
  vpc_id = aws_vpc.vpc-2.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [aws_vpc.vpc-1.cidr_block]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "peering-sg2"
  }
}

resource "aws_instance" "server-1" {
  ami = var.ami-1
  instance_type = var.instance-type
  key_name = var.key-1
  vpc_security_group_ids = [aws_security_group.peering-sg-1.id]
  subnet_id = aws_subnet.subnet-1.id

  tags = {
    Name = "server-1"
  }
}

resource "aws_instance" "server-2" {
  provider = aws.region-2
  ami = var.ami-2
  instance_type = var.instance-type
  key_name = var.key-2
  vpc_security_group_ids = [aws_security_group.peering-sg-2.id]
  subnet_id = aws_subnet.subnet-2.id

  tags = {
    Name = "server-2"
  }
}