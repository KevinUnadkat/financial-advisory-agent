# financial-advisory-agent  

## Overview  
The Financial Advisory Agent is an AI-powered chatbot that provides financial guidance based on a predefined knowledge base. It ensures responsible financial communication by following ethical guardrails.  

## Features  
- Retrieves financial information from a structured knowledge base.  
- Uses Gemini-2.0 AI for intelligent responses.  
- Implements security measures to avoid misleading financial claims.  
- Formats responses for clarity and readability.  

## Setup Instructions  

1. Clone the repository:

   git clone https://github.com/KevinUnadkat/financial-advisory-agent.git

2. Create a virtual environment and install dependencies:
   
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt

3. Run the agent:
   
   python agent.py


## Test Cases
Run unit tests using pytest:
   pytest test_agent.py
   
Key Tests:

Knowledge Base: Ensures financial data is loaded correctly.

Retrieval: Extracts relevant financial concepts from the knowledge base.

Guardrails: Blocks misleading investment advice.

Response Formatting: Ensures concise and structured answers.

Disclaimer
This AI agent provides general financial information and does not offer personalized investment advice. Consult a licensed financial advisor for specific guidance.