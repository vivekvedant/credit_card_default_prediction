resource "aws_instance" "test_server" {
  ami = var.ami
  key_name = var.key_name
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.webtraffic.id]
  subnet_id   = aws_subnet.public_subnet.id
  associate_public_ip_address   = true
  depends_on = [aws_key_pair.private-key]
}

