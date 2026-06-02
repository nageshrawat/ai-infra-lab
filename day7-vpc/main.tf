resource "aws_vpc" "main" {

  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "ai-infra-vpc"
  }
}
resource "aws_subnet" "public" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.1.0/24"

  availability_zone = "ap-south-1a"

  tags = {
    Name = "public-subnet"
  }
}
resource "aws_internet_gateway" "igw" {

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "ai-infra-igw"
  }
}

resource "aws_route_table" "public_rt" {

  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-route-table"
  }
}
resource "aws_route_table_association" "public_assoc" {

  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_security_group" "ssh_sg" {

  name        = "ssh-security-group"
  description = "Allow SSH access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH"

    from_port   = 22
    to_port     = 22
    protocol    = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {

    from_port   = 0
    to_port     = 0
    protocol    = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ssh-security-group"
  }
}
data "aws_ami" "amazon_linux" {

  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}
resource "aws_instance" "linux_server" {

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  subnet_id = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.ssh_sg.id
  ]

  key_name = "terraform-lab-key"

  associate_public_ip_address = true

  tags = {
    Name = "terraform-linux-server"
  }
}
output "instance_public_ip" {
  value = aws_instance.linux_server.public_ip
}

output "instance_private_ip" {
  value = aws_instance.linux_server.private_ip
}