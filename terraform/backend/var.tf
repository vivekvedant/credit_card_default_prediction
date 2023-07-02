variable "s3_name" {
  type = string
  default = "credit-default-data-versioning"
}
variable "dynamo_db_name"{
  type = string
  default = "state-lock"
}
variable "aws_region" {
  type = string
  default = "ap-south-1"
}



