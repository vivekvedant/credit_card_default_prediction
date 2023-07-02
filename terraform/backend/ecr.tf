module "ecr" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name = var.ecr_name

  repository_read_write_access_arns = [var.aws_arn_id]

  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 100 images",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["v"],
          countType     = "imageCountMoreThan",
          countNumber   = 100
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
  
}