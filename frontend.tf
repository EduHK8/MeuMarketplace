resource "aws_s3_bucket_object" "frontend_html" {
  bucket = aws_s3_bucket_acl.b_acl.bucket
  key    = "index.html"
  source = "${path.module}/index.html" 
  acl    = "public-read"
  content_type = "text/html"
}

resource "aws_s3_bucket_object" "frontend_css" {
  bucket = aws_s3_bucket_acl.b_acl.bucket
  key    = "style.css"
  source = "${path.module}/style.css"
  acl    = "public-read"
  content_type = "text/css"
}

resource "aws_s3_bucket_policy" "frontend_policy" {
  bucket = aws_s3_bucket_acl.b_acl.bucket

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = [
          aws_s3_bucket_object.frontend_html.id,
          aws_s3_bucket_object.frontend_css.id,
        ]
      },
    ]
  })
}