import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from bedrock_agentcore.tools.code_interpreter_client import CodeInterpreter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class CodeInterpreterAgent:
    def __init__(self):
        self.code_sessions = {}
        
    def get_code_interpreter(self, session_id):
        """Get or create a code interpreter session using AgentCore SDK"""
        if session_id not in self.code_sessions:
            try:
                code_client = CodeInterpreter('us-east-1')
                code_client.start()
                self.code_sessions[session_id] = code_client
                logger.info(f"Started new code interpreter session: {session_id}")
            except Exception as e:
                logger.error(f"Failed to start code session: {e}")
                return None
        return self.code_sessions[session_id]
    
    def execute_code(self, session_id, code, language="python"):
        """Execute code using the AgentCore SDK"""
        code_client = self.get_code_interpreter(session_id)
        if not code_client:
            return "Failed to start code interpreter session"
        
        try:
            response = code_client.invoke("executeCode", {
                "language": language,
                "code": code
            })
            
            # Extract results from stream
            results = []
            for event in response["stream"]:
                if "result" in event:
                    result = event["result"]
                    if "content" in result:
                        for content_item in result["content"]:
                            if content_item["type"] == "text":
                                results.append(content_item["text"])
            
            return "\n".join(results) if results else "Code executed successfully"
            
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return f"Error executing code: {str(e)}"
    
    def cleanup_session(self, session_id):
        """Clean up a code interpreter session"""
        if session_id in self.code_sessions:
            try:
                self.code_sessions[session_id].stop()
                del self.code_sessions[session_id]
                logger.info(f"Cleaned up session: {session_id}")
            except Exception as e:
                logger.error(f"Error cleaning up session {session_id}: {e}")
    
    def process_message(self, message, session_id):
        """Process user message and determine if code execution is needed"""
        message_lower = message.lower()
        
        # Check if user wants to execute code
        if any(keyword in message_lower for keyword in ['calculate', 'compute', 'analyze data', 'run code', 'execute']):
            # Extract code if present
            if '```' in message:
                code_blocks = message.split('```')
                if len(code_blocks) >= 3:
                    code = code_blocks[1]
                    # Remove language identifier if present
                    lines = code.strip().split('\n')
                    if lines[0] in ['python', 'py', 'javascript', 'js']:
                        code = '\n'.join(lines[1:])
                    else:
                        code = '\n'.join(lines)
                    
                    result = self.execute_code(session_id, code)
                    return f"Code execution result:\n{result}"
            
            # Generate code based on request
            if 'portfolio' in message_lower or 'investment' in message_lower:
                code = """
                    # Investment portfolio analysis
                    import numpy as np

                    # Sample portfolio data
                    stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
                    prices = [150, 2500, 300, 3200]
                    shares = [100, 10, 50, 5]

                    # Calculate portfolio value
                    portfolio_value = sum(price * share for price, share in zip(prices, shares))
                    print(f"Total Portfolio Value: ${portfolio_value:,.2f}")

                    # Calculate individual positions
                    for stock, price, share in zip(stocks, prices, shares):
                        position_value = price * share
                        percentage = (position_value / portfolio_value) * 100
                        print(f"{stock}: ${position_value:,.2f} ({percentage:.1f}%)")
                """
                result = self.execute_code(session_id, code)
                return f"Portfolio Analysis:\n{result}"
        
        # Default investment research response
        return self.generate_investment_response(message)
    
    def generate_investment_response(self, message):
        """Generate investment research response"""
        return f"""Based on your query about "{message}", here are some key investment considerations:

        • Market Analysis: Current market conditions suggest cautious optimism
        • Risk Assessment: Diversification remains crucial for portfolio stability  
        • Recommendation: Consider your risk tolerance and investment timeline

        Would you like me to run any calculations or data analysis? Just ask me to calculate or analyze something, or provide code in ```code blocks```.

        Example: "Calculate my portfolio performance" or "Analyze risk metrics for my holdings"
        """

# Initialize agent
agent = CodeInterpreterAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/invoke', methods=['POST'])
def invoke_agent():
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('sessionId', 'default')
        
        logger.info(f"Processing message for session {session_id}: {message}")
        
        response = agent.process_message(message, session_id)
        
        return jsonify({
            "response": response,
            "sessionId": session_id,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/cleanup/<session_id>', methods=['DELETE'])
def cleanup_session(session_id):
    """Cleanup endpoint for code interpreter sessions"""
    try:
        agent.cleanup_session(session_id)
        return jsonify({"message": f"Session {session_id} cleaned up"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
