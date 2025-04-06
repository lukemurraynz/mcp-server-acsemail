# basic import 
from mcp.server.fastmcp import FastMCP
import math
from azure.communication.email import EmailClient
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# instantiate an MCP server client
mcp = FastMCP("Hello World")

# DEFINE TOOLS

# Azure Communication Services configuration
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
ACS_SENDER_ADDRESS = os.getenv("ACS_SENDER_ADDRESS")

# Email tool
@mcp.tool()
def send_email(recipient: str, subject: str, content: str) -> str:
    """Send an email using Azure Communication Services
    
    Args:
        recipient: Email address of the recipient
        subject: Subject line of the email
        content: HTML content of the email
        
    Returns:
        A message indicating the status of the email sending operation
    """
    print(f"[INFO] Starting email sending process to: {recipient}")
    
    if not ACS_CONNECTION_STRING or ACS_CONNECTION_STRING == "your_acs_connection_string_here":
        print(f"[ERROR] ACS_CONNECTION_STRING is not configured properly: {ACS_CONNECTION_STRING}")
        return "Error: ACS_CONNECTION_STRING is not configured properly. Check your .env file."
    
    if not ACS_SENDER_ADDRESS or ACS_SENDER_ADDRESS == "DoNotReply@your-domain.azurecomm.net":
        print(f"[ERROR] ACS_SENDER_ADDRESS is not configured properly: {ACS_SENDER_ADDRESS}")
        return "Error: ACS_SENDER_ADDRESS is not configured properly. Check your .env file."
    
    print(f"[INFO] Email configuration validated. Sender: {ACS_SENDER_ADDRESS}")
    
    try:
        # Initialize the Email Client
        print(f"[INFO] Initializing Email Client with connection string")
        email_client = EmailClient.from_connection_string(ACS_CONNECTION_STRING)
        print(f"[INFO] Email Client initialized successfully")
       
        # Create the email content
        print(f"[INFO] Creating email message with subject: {subject}")
        message = {
            "content": {
                "subject": subject,
                "plainText": content,
                "html": content
            },
            "recipients": {
                "to": [
                    {
                        "address": recipient,
                        "displayName": "Email Recipient"
                    }
                ]
            },
            "senderAddress": ACS_SENDER_ADDRESS
        }
        print(f"[INFO] Email message created successfully")
        
        # Send the email
        print(f"[INFO] Beginning email send operation")
        poller = email_client.begin_send(message)
        print(f"[INFO] Email send operation initiated, waiting for result")
        result = poller.result()
        
        # Debug - inspect result structure
        print(f"[DEBUG] Result type: {type(result)}")
        print(f"[DEBUG] Result content: {result}")
        print(f"[DEBUG] Result dir: {dir(result)}")
        
        # Handle result as dictionary if that's what's returned
        if isinstance(result, dict) and 'id' in result:
            message_id = result.get('id', 'unknown')
            print(f"[SUCCESS] Email sent successfully to {recipient}. Message ID: {message_id}")
            return f"Email sent to {recipient} successfully! Message ID: {message_id}"
        # Handle result as object with message_id attribute
        elif hasattr(result, 'message_id'):
            print(f"[SUCCESS] Email sent successfully to {recipient}. Message ID: {result.message_id}")
            return f"Email sent to {recipient} successfully! Message ID: {result.message_id}"
        # Handle any other type of successful result
        else:
            print(f"[SUCCESS] Email sent successfully to {recipient}.")
            return f"Email sent to {recipient} successfully!"
    except Exception as e:
        print(f"[ERROR] Failed to send email: {str(e)}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        return f"Failed to send email: {str(e)}"

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return int(a + b)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    return float(math.tan(a))

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)



# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
    
 
 # execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")