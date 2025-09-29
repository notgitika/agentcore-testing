"""
Investment bot with AgentCore Gateway integration for market data and paper trading.
"""

import os
import json
import asyncio
import httpx
import requests
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

# Gateway configuration - hardcoded for now
GATEWAY_URL = "https://investment-bot-gateway-hnjyvl28zn.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
CLIENT_ID = "e5nmv8ct97p1gk15t9dgq2dvc"
CLIENT_SECRET = "1ava9f5ubmr3lmasie48tai24381amfrfjcbvvc027kngks37dk3"
TOKEN_URL = "https://agentcore-4d4a0781.auth.us-east-1.amazoncognito.com/oauth2/token"

def get_access_token():
    """Get OAuth access token for Gateway"""
    response = requests.post(
        TOKEN_URL,
        data=f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}",
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    return response.json()['access_token']

async def list_gateway_tools():
    """List available tools in Gateway"""
    try:
        token = get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GATEWAY_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list"
                }
            )
            
            result = response.json()
            return result.get('result', {}).get('tools', [])
    except Exception as e:
        return {"error": f"Failed to list tools: {str(e)}"}

async def call_gateway_tool(tool_name: str, arguments: dict):
    """Call Gateway tools"""
    try:
        token = get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GATEWAY_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                }
            )
            
            result = response.json()
            if 'error' in result:
                return {"error": f"Tool error: {result['error']}"}
            
            return result.get('result')
    except Exception as e:
        return {"error": f"Gateway connection error: {str(e)}"}

@app.entrypoint
def invoke(payload, context):
    """Investment bot with market data and trading capabilities"""
    user_message = payload.get("input", {}).get("prompt", "").lower()
    
    # Test Gateway connection
    if "test" in user_message or "hello" in user_message:
        try:
            token = get_access_token()
            return f"✅ Gateway connection successful! Token obtained. Ready for investment queries."
        except Exception as e:
            return f"❌ Gateway connection failed: {str(e)}"
    
    # List available tools
    elif "tools" in user_message or "list" in user_message:
        tools = asyncio.run(list_gateway_tools())
        return f"Available Gateway tools: {json.dumps(tools, indent=2)}"
    
    # Price lookup
    elif "price" in user_message or "quote" in user_message:
        # Extract symbol (simplified)
        words = user_message.split()
        symbol = None
        for word in words:
            if word.upper() in ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META']:
                symbol = word.upper()
                break
        
        if symbol:
            result = asyncio.run(call_gateway_tool("AlphaVantage___getPrice", {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": "OCSN786ETHEWKP42"
            }))
            return f"Price data for {symbol}: {json.dumps(result, indent=2)}"
        else:
            return "Please specify a stock symbol (e.g., 'price of AAPL')"
    
    # Trading
    elif "buy" in user_message or "sell" in user_message:
        # Extract trade details
        side = "buy" if "buy" in user_message else "sell"
        
        # Extract symbol from message
        words = user_message.split()
        symbol = None
        for word in words:
            if word.upper() in ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META']:
                symbol = word.upper()
                break
            elif word.lower() == 'tesla':
                symbol = 'TSLA'
                break
            elif word.lower() == 'apple':
                symbol = 'AAPL'
                break
        
        if not symbol:
            symbol = "AAPL"  # Default fallback
        
        qty = 1  # Default quantity
        
        result = asyncio.run(call_gateway_tool("Alpaca___placeOrder", {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "type": "market",
            "time_in_force": "day"
        }))
        return f"Order placed: {side} {qty} shares of {symbol}. Result: {json.dumps(result, indent=2)}"
    
    return "I'm your investment bot with Gateway integration! Try: 'test connection', 'price of AAPL', or 'buy Tesla'"

if __name__ == "__main__":
    app.run()
