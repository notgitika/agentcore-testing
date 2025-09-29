"""
Setup AgentCore Gateway for investment bot with Alpha Vantage and Alpaca integration.
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json

# ADD YOUR API KEYS HERE:
ALPHA_VANTAGE_KEY = "OCSN786ETHEWKP42"
ALPACA_KEY_ID = "PKE6OO032H0M3KMS8TZH"
ALPACA_SECRET = "UfYTKzaUGUXhMSiWbsVugb50ef5UFOX0w54YofnJ"

client = GatewayClient(region_name='us-east-1')

print("Creating OAuth authorizer...")
cognito = client.create_oauth_authorizer_with_cognito("investment-bot")

print("Creating Gateway...")
gateway = client.create_mcp_gateway(
    name="investment-bot-gateway",
    role_arn=None,
    authorizer_config=cognito['authorizer_config'],
    enable_semantic_search=True
)

# print("Adding Alpha Vantage target...")
# target = client.create_mcp_gateway_target(
#     gateway=gateway,
#     name="AlphaVantage",
#     target_type="openApiSchema",
#     target_payload={
#         "inlinePayload": {
#             "openai": "3.0.3",
#             "info": {"title": "Investment Tools", "version": "1.0"},
#             "servers": [{"url": "https://www.alphavantage.co"}],
#             "paths": {
#                 "/query": {
#                     "get": {
#                         "operationId": "getPrice",
#                         "parameters": [
#                             {"name": "function", "in": "query", "required": True, "schema": {"type": "string"}},
#                             {"name": "symbol", "in": "query", "required": True, "schema": {"type": "string"}},
#                             {"name": "apikey", "in": "query", "required": True, "schema": {"type": "string", "default": ALPHA_VANTAGE_KEY}}
#                         ],
#                         "responses": {"200": {"description": "OK"}}
#                     }
#                 }
#             }
#         }
#     }
# )

# print(f"Gateway URL: {gateway['gatewayUrl']}")

# # Save config for agent
# config = {
#     "gateway_url": gateway['gatewayUrl'],
#     "client_id": cognito['client_info']['client_id'],
#     "client_secret": cognito['client_info']['client_secret'],
#     "token_endpoint": cognito['client_info']['token_endpoint']
# }

# with open("investment_gateway_config.json", "w") as f:
#     json.dump(config, f, indent=2)

# print("✅ Gateway configured with API keys embedded")
