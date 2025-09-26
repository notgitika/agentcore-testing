#!/usr/bin/env python3

import boto3
import json
import uuid
from datetime import datetime

# Agent configuration
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:998846730471:runtime/first_testing_agent-qt0qXTEqu4"
REGION_NAME = "us-east-1"

def generate_session_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4()).replace('-', '')[:8]
    return f"memory-test-{timestamp}-{unique_id}"

def test_memory_agent():
    client = boto3.client('bedrock-agentcore', region_name=REGION_NAME)
    session_id = generate_session_id()
    actor_id = "test-user"
    
    print(f"🧪 Testing Memory Agent")
    print(f"Session ID: {session_id}")
    print(f"Actor ID: {actor_id}")
    print("=" * 50)
    
    # Test sequence to verify memory works
    test_sequence = [
        "Hi, I'm interested in conservative dividend-paying stocks. Please remember this preference.",
        "What investment preferences did I just tell you?",
        "Based on my preferences, should I invest in Tesla?",
        "What do you remember about my investment style?"
    ]
    
    for i, prompt in enumerate(test_sequence, 1):
        print(f"\n🔍 Test {i}: {prompt}")
        print("-" * 30)
        
        try:
            payload = json.dumps({
                "input": {
                    "prompt": prompt,
                    "sessionId": session_id,
                    "actorId": actor_id
                }
            })
            
            response = client.invoke_agent_runtime(
                agentRuntimeArn=AGENT_RUNTIME_ARN,
                runtimeSessionId=session_id,
                payload=payload,
                qualifier="DEFAULT"
            )
            
            response_body = response['response'].read()
            result = json.loads(response_body)
            
            # Extract response text
            if 'output' in result and 'message' in result['output']:
                message = result['output']['message']
                if hasattr(message, 'content') and message.content:
                    response_text = message.content[0].text
                else:
                    response_text = str(message)
                print(f"✅ Agent: {response_text}")
            else:
                print(f"✅ Raw response: {json.dumps(result, indent=2)}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Small delay between requests
        import time
        time.sleep(2)

if __name__ == "__main__":
    test_memory_agent()
