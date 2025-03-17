import os
import pytest
import json
from langchain.schema import Document
from agent import knowledge_base, initialize_model, retrieve, guardrails, format_response, chat, validate_numbers

# Test Data
mock_data = [
    {"text": "A stock is a type of investment representing ownership in a company.", "metadata": {"source": "SEC"}},
    {"text": "Diversification helps in reducing investment risk.", "metadata": {"source": "Finance Guide"}}
]

mock_documents = [
    Document(page_content=item["text"], metadata=item["metadata"]) for item in mock_data
]


def test_knowledge_base():
    with open("mock_knowledge.json", "w", encoding="utf-8") as f:
        json.dump(mock_data, f)

    docs = knowledge_base("mock_knowledge.json")
    assert len(docs) == 2
    assert docs[0].page_content.startswith("A stock is a type")
    
    os.remove("mock_knowledge.json")  

def test_retrieve_valid():
    question = "What is a stock?"
    response = retrieve(question, mock_documents)
    assert "stock is a type of investment" in response


def test_guardrails_safe():
    response = guardrails("Stocks can be a good long-term investment.")
    assert response == "Stocks can be a good long-term investment."

def test_guardrails_restricted():
    response = guardrails("Guaranteed returns of 10% per month.")
    assert response == "I cannot provide financial guarantees or insider trading information. Please consult a licensed advisor."

def test_format_response():
    """Check that responses are properly formatted."""
    response = "Investing early helps.\nInvesting early helps.\nStart with a 401(k)."
    formatted = format_response(response)
    
    assert "Investing early helps." in formatted
    assert "Start with a 401(k)." in formatted
    assert "Disclaimer: This is general financial information" in formatted

def test_validate_numbers():
    """Ensure numerical values trigger disclaimers."""
    response = validate_numbers("The stock price is expected to rise by 15%.")
    assert "Note: Financial figures are approximations" in response

def test_validate_no_numbers():
    """Ensure non-numerical responses remain unchanged."""
    response = validate_numbers("Stock prices fluctuate based on demand.")
    assert response == "Stock prices fluctuate based on demand."

# Edge Case Tests
def test_empty_query():
    """Ensure empty queries return appropriate messages."""
    response = retrieve("", mock_documents)
    assert response == "I could not find relevant information in my knowledge base."

def test_large_query():
    """Ensure very large queries do not break the system."""
    question = "What is" + " finance?" * 1000  
    response = retrieve(question, mock_documents)

    assert isinstance(response, str) and len(response) > 0