
terraform {
  backend "s3"{
    bucket = "credit-default-data-versioning"
    dynamodb_table = "state-lock"
    key = "global/mystatefile/terraform.tfstate"
    region = "ap-south-1"
    encrypt = true
  }
  required_providers {
    ansible = {
      version = "~> 1.1.0"
      source  = "ansible/ansible"
    }
  }
}


module "ec2" {
  source = "./ec2"
}

variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}
variable "aws_account_id" {}
variable "image_tag" {}
variable "mongodb_url" {}

module "ansible" {
  source = "./ansible"
  aws_instance_ip = module.ec2.aws_instance_ip
  aws_vpc_id = module.ec2.aws_vpc_id
  pvt_key = module.ec2.private_key_content
  aws_access_key_id = "${var.aws_access_key_id}"
  aws_secret_access_key = "${var.aws_secret_access_key}"
  aws_account_id = "${var.aws_account_id}"
  mongodb_url = "${var.mongodb_url}"
  image_tag = "${var.image_tag}"
}