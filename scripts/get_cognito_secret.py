"""
Get Cognito client secret for Gateway OAuth.
"""

import boto3

# From your logs: User Pool: us-east-1_VgJkKmnc6, Client: e5nmv8ct97p1gk15t9dgq2dvc
USER_POOL_ID = "us-east-1_VgJkKmnc6"
CLIENT_ID = "e5nmv8ct97p1gk15t9dgq2dvc"

cognito = boto3.client('cognito-idp', region_name='us-east-1')

try:
    response = cognito.describe_user_pool_client(
        UserPoolId=USER_POOL_ID,
        ClientId=CLIENT_ID
    )
    
    client_secret = response['UserPoolClient'].get('ClientSecret')
    if client_secret:
        print(f"CLIENT_ID: {CLIENT_ID}")
        print(f"CLIENT_SECRET: {client_secret}")
        print(f"TOKEN_URL: https://agentcore-4d4a0781.auth.us-east-1.amazoncognito.com/oauth2/token")
    else:
        print("No client secret found - client may not be configured for client credentials flow")
        
except Exception as e:
    print(f"Error: {e}")
    print("Make sure you have the correct User Pool ID and Client ID")
