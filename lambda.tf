resource "aws_iam_role" "lambda_role" {
  name               = "lambda_execution_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "purchase_simulation" {
  filename      = "lambda_function.zip"
  function_name = "purchaseSimulation"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.purchase_queue.id
    }
  }
}

resource "aws_lambda_function" "check_status_function" {
  filename      = "${path.module}/check_status_function.zip"
  function_name = "checkPurchaseStatus"
  role          = aws_iam_role.lambda_role.arn
  handler       = "check_status_function.lambda_handler"
  runtime       = "python3.8"

  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.purchase_queue.id
    }
  }
}