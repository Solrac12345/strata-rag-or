# EN: IAM role and policies for the Lambda function
# FR: Rôle et politiques IAM pour la fonction Lambda

resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_name}-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# EN: Basic Lambda execution (CloudWatch Logs)
# FR: Exécution Lambda de base (CloudWatch Logs)
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# EN: Bedrock invoke permission
# FR: Permission d'invocation Bedrock
resource "aws_iam_role_policy" "bedrock_invoke" {
  name = "${var.project_name}-bedrock-invoke"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["bedrock:InvokeModel"]
      Resource = "*"
    }]
  })
}

# EN: DynamoDB read/write permission
# FR: Permission de lecture/écriture DynamoDB
resource "aws_iam_role_policy" "dynamodb_access" {
  name = "${var.project_name}-dynamodb-access"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ]
      Resource = aws_dynamodb_table.docs.arn
    }]
  })
}

# EN: S3 read permission for knowledge base
# FR: Permission de lecture S3 pour la base de connaissances
resource "aws_iam_role_policy" "s3_read" {
  name = "${var.project_name}-s3-read"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:ListBucket"]
      Resource = ["arn:aws:s3:::${var.project_name}-kb-${var.environment}/*"]
    }]
  })
}