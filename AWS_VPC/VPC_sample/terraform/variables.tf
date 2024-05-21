variable "region" {
    type = string
}

variable "vpc-cidr" {
  type = string
}

variable "public-subnet-cidr" {
  type = string
}

variable "private-subnet-cidr" {
  type = string
}

variable "public-subnet-az" {
  type = string
}

variable "private-subnet-az" {
  type = string
}

variable "ami" {
  type = string
}

variable "instance-type" {
  type = string
}

variable "key-name" {
  type = string
}