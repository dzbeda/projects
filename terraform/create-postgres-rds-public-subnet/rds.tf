## VPC
resource "aws_vpc" "vpc-main" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags       = {
    Name = "rds"
  }
}

## Internet GW
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc-main.id
  tags = {
    Name = "rds"
  }
}

## Public Subnet ##

resource "aws_subnet" "public_subnet" {
  count = 2
  cidr_block = var.public-subnet-block[count.index]
  availability_zone = var.availability_zone[count.index]
  vpc_id = aws_vpc.vpc-main.id
  map_public_ip_on_launch = true
  tags = {
    Name = "rds"
  }
}

resource "aws_route_table" "route-table-public-subnet" {
  vpc_id = aws_vpc.vpc-main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "rds"
  }
}

resource "aws_route_table_association" "public-subnet" {
  count = 1
  route_table_id = aws_route_table.route-table-public-subnet.id
  subnet_id = aws_subnet.public_subnet.*.id[count.index]
}

## APB security group
resource "aws_security_group" "rds" {
  name ="rds-security-group"
  vpc_id = aws_vpc.vpc-main.id
  ## Incoming roles
  ingress {
    from_port = 5432
    to_port =  5432
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow DB  access"
  }
  ingress {
    from_port = 22
    to_port =  22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow DB ssh access"
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  tags = {
    Name = "rds"
  }
}

resource "aws_db_subnet_group" "rds" {
  name       = "rds"
  subnet_ids = aws_subnet.public_subnet.*.id

  tags = {
    Name = "rds"
  }
}

resource "aws_db_instance" "kandula_postgres" {
  allocated_storage    = 10
  identifier           = "db1"
  engine               = "postgres"
  engine_version       = "12.7"
  instance_class       = "db.t3.micro"
  username             = "postgres"
  password             = "thispassword"
  backup_retention_period = 0 #if replica is needed - more than 1
  vpc_security_group_ids = [aws_security_group.rds.id]
  name = "main"
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  skip_final_snapshot  = true
  publicly_accessible    = true
}