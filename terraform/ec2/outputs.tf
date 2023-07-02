output  "aws_instance_ip" {
  value = "${aws_instance.test_server.public_ip}"
}
output "aws_vpc_id"{
  value = "${aws_vpc.main.id}"
}

output "private_key_content"{
    value = tls_private_key.rsa.private_key_pem
}
