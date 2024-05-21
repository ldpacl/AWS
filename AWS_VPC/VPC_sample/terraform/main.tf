provider "aws" {
  region = var.region
}

resource "aws_vpc" "tf-vpc" {
  cidr_block = var.vpc-cidr
  tags = {
    Name = "tf-vpc"
  }
}

resource "aws_subnet" "public-subnet"{
  vpc_id = aws_vpc.tf-vpc.id
  cidr_block = var.public-subnet-cidr
  availability_zone = var.public-subnet-az
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

resource "aws_subnet" "private-subnet"{
  vpc_id = aws_vpc.tf-vpc.id
  cidr_block = var.private-subnet-cidr
  availability_zone = var.private-subnet-az

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.tf-vpc.id

  tags = {
    Name = "tf-igw"
  }
}

resource "aws_eip" "nat-aws_eip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat-aws_eip.id
  subnet_id = aws_subnet.public-subnet.id
  depends_on = [ aws_internet_gateway.igw ]
}

resource "aws_route_table" "public-subnet-rt" {
  vpc_id = aws_vpc.tf-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table_association" "rt-association" {
  subnet_id = aws_subnet.public-subnet.id
  route_table_id = aws_route_table.public-subnet-rt.id
}

resource "aws_route_table" "private-subnet-rt" {
  vpc_id = aws_vpc.tf-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
  tags = {
    Name = "private-rt"
  }
}

resource "aws_route_table_association" "rt-association2" {
  subnet_id = aws_subnet.private-subnet.id
  route_table_id = aws_route_table.private-subnet-rt.id
}

resource "aws_security_group" "public-sg" {
  name = "public-sg"
  vpc_id = aws_vpc.tf-vpc.id

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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
    Name = "public-sg"
  }
}

resource "aws_security_group" "private-sg" {
  name = "private-sg"
  vpc_id = aws_vpc.tf-vpc.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "private-sg"
  }
}

resource "aws_instance" "public-server" {
  ami = var.ami
  instance_type = var.instance-type
  key_name = var.key-name
  vpc_security_group_ids = [aws_security_group.public-sg.id]
  subnet_id = aws_subnet.public-subnet.id

  tags = {
    Name = "public-server"
  }
}

resource "aws_instance" "private-server" {
  ami = var.ami
  instance_type = var.instance-type
  key_name = var.key-name
  vpc_security_group_ids = [aws_security_group.private-sg.id]
  subnet_id = aws_subnet.private-subnet.id

  tags = {
    Name = "private-server"
  }
}