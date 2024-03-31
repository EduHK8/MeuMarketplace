terraform {
    required_providers {
        aws={
            source = "hashicorp/aws"
            version = "~> 3.27"
        }
    }
}

variable "localstack_endpoint" {
  type = string
  default = "http://localhost:4566"
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_force_path_style         = true
  endpoints {
    s3 = "http://localhost:4566"
    iam         = "http://localhost:4566"
    lambda = "http://localhost:4566"
    sqs = "http://localhost:4566"
  }
}

resource "aws_s3_bucket_acl" "b_acl" {
  bucket = "onexlab-bucket-terraform"
  acl    = "public-read"
}

resource "aws_s3_bucket" "b" {
  bucket = "onexlab-bucket-terraform"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_sqs_queue" "purchase_queue" {
  name                      = "purchase-queue"
  delay_seconds             = 0
  max_message_size          = 2048
  message_retention_seconds = 86400  # 1 dia
  visibility_timeout_seconds = 30
}

resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "lambda_sqs_policy"
  description = "Policy to allow Lambda to send and receive messages from SQS"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:GetQueueUrl"
        ],
        Resource = aws_sqs_queue.purchase_queue.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
}
