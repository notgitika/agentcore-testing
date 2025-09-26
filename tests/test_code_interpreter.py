#!/usr/bin/env python3
import requests
import json

def test_code_interpreter(agent_url):
    """Test the Code Interpreter functionality"""
    
    print("🧪 Testing Bedrock Agent Core with Code Interpreter Tool")
    print("=" * 60)
    
    # Test 1: Portfolio calculation
    print("\n1. Testing Portfolio Calculation:")
    response = requests.post(f"{agent_url}/invoke", json={
        "message": "Calculate my portfolio performance with these holdings: AAPL 100 shares at $150, GOOGL 10 shares at $2500",
        "sessionId": "code-test-001"
    })
    print(f"Response: {response.json()['response']}")
    
    # Test 2: Direct code execution
    print("\n2. Testing Direct Code Execution:")
    code_message = """
        Execute this code:
        ```python
        import math

        # Calculate compound interest
        principal = 10000
        rate = 0.07
        time = 10

        compound_amount = principal * (1 + rate) ** time
        interest_earned = compound_amount - principal

        print(f"Principal: ${principal:,.2f}")
        print(f"Rate: {rate*100}%")
        print(f"Time: {time} years")
        print(f"Final Amount: ${compound_amount:,.2f}")
        print(f"Interest Earned: ${interest_earned:,.2f}")
        ```
    """
    
    response = requests.post(f"{agent_url}/invoke", json={
        "message": code_message,
        "sessionId": "code-test-002"
    })
    print(f"Response: {response.json()['response']}")
    
    # Test 3: Data analysis request
    print("\n3. Testing Data Analysis Request:")
    response = requests.post(f"{agent_url}/invoke", json={
        "message": "Analyze risk metrics for a diversified portfolio",
        "sessionId": "code-test-003"
    })
    print(f"Response: {response.json()['response']}")

if __name__ == "__main__":
    # Replace with your actual agent endpoint
    agent_url = input("Enter your agent endpoint URL (or press Enter for localhost:8080): ").strip()
    if not agent_url:
        agent_url = "http://localhost:8080"
    
    try:
        test_code_interpreter(agent_url)
    except Exception as e:
        print(f"Error: {e}")
