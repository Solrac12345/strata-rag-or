# EN: DynamoDB table for document metadata / conversation history
# FR: Table DynamoDB pour les métadonnées de documents / historique des conversations

resource "aws_dynamodb_table" "docs" {
  name         = "${var.project_name}-docs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}