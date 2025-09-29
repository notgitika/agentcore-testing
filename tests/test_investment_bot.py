"""
Test script for investment bot with Gateway integration.
"""

import boto3
import json
import uuid

# Configuration
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:998846730471:runtime/first_testing_agent-qt0qXTEqu4"
REGION = "us-east-1"

def test_investment_bot(prompt):
    """Test the investment bot with a specific prompt"""
    client = boto3.client('bedrock-agentcore', region_name=REGION)
    
    # Generate unique session ID
    session_id = f"test-session-{uuid.uuid4().hex}"
    
    payload = json.dumps({
        "input": {"prompt": prompt}
    })
    
    try:
        print(f"🧪 Testing: '{prompt}'")
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=payload,
            qualifier="DEFAULT"
        )
        
        response_body = response['response'].read()
        response_data = json.loads(response_body)
        
        print(f"✅ Response: {json.dumps(response_data, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 50)

if __name__ == "__main__":
    # Test Gateway connection
    test_investment_bot("test connection")
    
    # List available tools
    test_investment_bot("list tools")
    
    # # Test price lookup
    test_investment_bot("price of AAPL")
    
    # Test trading
    test_investment_bot("buy AMZN 2 shares")
    
    # Test general query
    test_investment_bot("What can you do?")
