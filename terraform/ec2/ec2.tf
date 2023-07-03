resource "aws_instance" "ec2_instance" {
  ami = var.ami
  key_name = var.key_name
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.webtraffic.id]
  subnet_id   = aws_subnet.public_subnet.id
  associate_public_ip_address   = true
  depends_on = [aws_key_pair.private-key]
  
  root_block_device {
    volume_size           = "20"
    volume_type           = "gp2"
    encrypted             = true
    delete_on_termination = true
  }
}

