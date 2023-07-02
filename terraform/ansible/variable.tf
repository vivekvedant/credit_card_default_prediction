
variable "pvt_key"{
  type = string
  description = "private key content"
}

variable "aws_instance_ip" {
  type = string
  description  = "aws instance IP address"
}
variable "aws_vpc_id"{
  type = string
  description = "Id of vpc"
}

variable "aws_account_id" {
  type = string
  description = "aws acount id"
}

variable "aws_access_key_id" {
  type = string
  description = "aws access key id"
}
variable "mongodb_url" {
  type = string
  description = "url of mongodb"
  
}

variable "aws_secret_access_key" {
  type = string
  description = "aws secret access key"
}

variable "image_tag"{
  type = string
}

