# EN: API Gateway (HTTP API) fronting the Lambda function
# FR: API Gateway (HTTP API) devant la fonction Lambda

resource "aws_apigatewayv2_api" "api" {
  name          = "${var.project_name}-api-${var.environment}"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.orchestrator.invoke_arn
  payload_format_version = "2.0"
}

# EN: POST /orchestrate route
# FR: Route POST /orchestrate
resource "aws_apigatewayv2_route" "orchestrate" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "POST /orchestrate"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# EN: GET /health route
# FR: Route GET /health
resource "aws_apigatewayv2_route" "health" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# EN: Allow API Gateway to invoke Lambda
# FR: Permettre à API Gateway d'invoquer Lambda
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.orchestrator.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}

# EN: Output the API endpoint URL
# FR: Afficher l'URL de l'endpoint API
output "api_endpoint" {
  value = aws_apigatewayv2_api.api.api_endpoint
}