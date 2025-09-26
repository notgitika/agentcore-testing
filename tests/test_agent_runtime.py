#!/usr/bin/env python3

import boto3
import json
import uuid
from datetime import datetime

AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:998846730471:runtime/first_testing_agent-qt0qXTEqu4" # My Agent ARN
REGION_NAME = "us-east-1"

def generate_session_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4()).replace('-', '')
    return f"test-session-{timestamp}-{unique_id}"

def test_agent(prompt):
    try:
        client = boto3.client('bedrock-agentcore', region_name=REGION_NAME)
        session_id = generate_session_id()
        
        payload = json.dumps({
            "input": {"prompt": prompt}
        })
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=payload,
            qualifier="DEFAULT"
        )
        
        response_body = response['response'].read()
        result = json.loads(response_body)
        
        print(f"✅ Response: {json.dumps(result, indent=2)}")
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Test cases
    test_cases = [
        "What can you do?",
        "Hello, how are you?",
        "Tell me about investment strategies"
    ]
    
    for prompt in test_cases:
        print(f"\n🧪 Testing: '{prompt}'")
        test_agent(prompt)
        print("-" * 50)
