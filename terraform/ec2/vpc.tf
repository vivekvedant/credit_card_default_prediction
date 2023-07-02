resource "aws_vpc" "main" {
  cidr_block           = "172.0.0.0/16"
  tags = {
    Name = "main"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block        = "172.0.1.0/24"
  availability_zone = "ap-south-1a"

  tags = {
    Name = "public_subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block        = "172.0.2.0/24"
  availability_zone = "ap-south-1a"

  tags = {
    Name = "private_subnet"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}


resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rt_association" {
  subnet_id = aws_subnet.public_subnet.id
  route_table_id =  aws_route_table.public_route_table.id
}
