"""
Get OAuth token for Gateway access.
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json

client = GatewayClient(region_name='us-east-1')

# You'll need the client info from the Cognito setup
# From your logs, the client ID was: e5nmv8ct97p1gk15t9dgq2dvc
# But we need the client secret too

print("To get the token, we need the Cognito client info from the setup.")
print("Check your previous setup logs for the client_info details.")
print("Or we can test without token first to see what happens.")
