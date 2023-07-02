resource "aws_dynamodb_table" "statelock" {
  name = var.dynamo_db_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"
  attribute{
    name = "LockID"
    type = "S"
  }
}
