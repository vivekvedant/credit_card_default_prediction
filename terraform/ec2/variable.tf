
variable "key_name" {
  type = string
  default = "private-key"
}

variable "ami" {
  type = string
  default = "ami-0f5ee92e2d63afc18"
}

variable "instance_type" {
    type = string
    default = "t2.micro"
}


variable "ingress_security_group" {
  type = list(object({
    description = string
    from_port = number
    to_port   = number
    protocol  = string
    cidr_blocks = list(string) 
    ipv6_cidr_blocks = list(string)

  }))
  default = [
  {
    description     ="HTTPS"
    from_port       =443
    to_port          = 443
    protocol        = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  },
  {
    description      = "HTTP"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  },
  {
    description      = "SSH"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  ]
}
