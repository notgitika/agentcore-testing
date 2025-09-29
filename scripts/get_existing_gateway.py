"""
Get existing Gateway info for investment bot.
"""

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
import json

client = GatewayClient(region_name='us-east-1')

# List existing gateways
print("Finding existing Gateway...")
gateways = client.client.list_gateways()
print(f"Response: {gateways}")

for gateway in gateways.get('items', []):
    if 'investment-bot' in gateway['name']:
        print(f"Found Gateway: {gateway['name']}")
        gateway_url = f"https://{gateway['gatewayId']}.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
        print(f"Gateway URL: {gateway_url}")
        
        # Save the gateway URL
        config = {
            "gateway_url": gateway_url,
            "gateway_name": gateway['name'],
            "gateway_id": gateway['gatewayId']
        }
        
        with open("investment_gateway_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Gateway config saved!")
        break
else:
    print("No investment-bot gateway found")
