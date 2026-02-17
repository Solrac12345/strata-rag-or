# EN: Lambda function for the StrataRAG orchestrator
# FR: Fonction Lambda pour l'orchestrateur StrataRAG

resource "aws_lambda_function" "orchestrator" {
  function_name = "${var.project_name}-orchestrator-${var.environment}"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "infrastructure.aws.lambda_handler.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  # EN: Placeholder — replace with S3 bucket/key or filename for real deployments
  # FR: Placeholder — remplacer par un bucket/clé S3 ou un fichier pour les vrais déploiements
  filename         = "lambda.zip"
  source_code_hash = filebase64sha256("lambda.zip")

  environment {
    variables = {
      APP_ENV          = var.environment
      LOG_LEVEL        = "info"
      AWS_REGION       = var.aws_region
      BEDROCK_USE_REAL = "true"
      USE_IN_MEMORY_DB = "false"
      DYNAMODB_TABLE   = aws_dynamodb_table.docs.name
      EMBEDDING_DIM    = "256"
      RETRIEVER_TOP_K  = "3"
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}