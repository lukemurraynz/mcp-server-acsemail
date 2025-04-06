# basic import 
from mcp.server.fastmcp import FastMCP
import logging
from azure.communication.email import EmailClient
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("acs-email-sender")

# Load environment variables
load_dotenv()

# Azure Communication Services configuration
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
ACS_SENDER_ADDRESS = os.getenv("ACS_SENDER_ADDRESS")

# Validation at startup
def validate_config() -> bool:
    """Validate the required configuration is present"""
    if not ACS_CONNECTION_STRING or ACS_CONNECTION_STRING == "your_acs_connection_string_here":
        logger.error(f"ACS_CONNECTION_STRING is not configured properly")
        return False
    
    if not ACS_SENDER_ADDRESS or ACS_SENDER_ADDRESS == "DoNotReply@your-domain.azurecomm.net":
        logger.error(f"ACS_SENDER_ADDRESS is not configured properly")
        return False
    
    logger.info(f"Email configuration validated. Sender: {ACS_SENDER_ADDRESS}")
    return True

# Cache the email client to avoid recreating it for each request
_email_client: Optional[EmailClient] = None

def get_email_client() -> Optional[EmailClient]:
    """Get or create an EmailClient instance"""
    global _email_client
    if _email_client is None:
        try:
            _email_client = EmailClient.from_connection_string(ACS_CONNECTION_STRING)
            logger.info("Email Client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Email Client: {str(e)}")
            return None
    return _email_client

# instantiate an MCP server client
mcp = FastMCP("Email Sender")

# DEFINE TOOLS

@mcp.tool(name="send_email")  
def send_email(recipient: str, subject: str, content: str) -> str:
    """Send all emails using Azure Communication Services
    
    Args:
        recipient: Email address of the recipient
        subject: Subject line of the email
        content: HTML content of the email
        
    Returns:
        A message indicating the status of the email sending operation
    """
    logger.info(f"Starting email sending process to: {recipient}")
    
    # Validate configuration
    if not validate_config():
        return "Error: Email service is not configured properly. Check your .env file."
    
    # Get email client
    email_client = get_email_client()
    if not email_client:
        return "Error: Unable to initialize email client"
    
    try:
        # Create the email message
        logger.info(f"Creating email message with subject: {subject}")
        message = create_email_message(recipient, subject, content)
        
        # Send the email
        logger.info(f"Beginning email send operation")
        poller = email_client.begin_send(message)
        logger.info(f"Email send operation initiated, waiting for result")
        result = poller.result()
        
        return process_email_result(result, recipient)
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}", exc_info=True)
        return f"Failed to send email: {str(e)}"

def create_email_message(recipient: str, subject: str, content: str) -> Dict[str, Any]:
    """Create an email message for Azure Communication Services"""
    return {
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

def process_email_result(result: Any, recipient: str) -> str:
    """Process the result from an email send operation"""
    if isinstance(result, dict) and 'id' in result:
        message_id = result.get('id', 'unknown')
        logger.info(f"Email sent successfully to {recipient}. Message ID: {message_id}")
        return f"Email sent to {recipient} successfully! Message ID: {message_id}"
    elif hasattr(result, 'message_id'):
        logger.info(f"Email sent successfully to {recipient}. Message ID: {result.message_id}")
        return f"Email sent to {recipient} successfully! Message ID: {result.message_id}"
    else:
        logger.info(f"Email sent successfully to {recipient}.")
        return f"Email sent to {recipient} successfully!"

@mcp.tool(name="send_email_with_attachments")
def send_email_with_attachments(recipient: str, subject: str, content: str, attachments: list) -> str:
    """Send email with file attachments using Azure Communication Services
    
    Args:
        recipient: Email address of the recipient
        subject: Subject line of the email
        content: HTML content of the email
        attachments: List of file paths to attach
        
    Returns:
        A message indicating the status of the email sending operation
    """
    logger.info(f"Starting email sending process with attachments to: {recipient}")
    
    # Validate configuration
    if not validate_config():
        return "Error: Email service is not configured properly. Check your .env file."
    
    # Get email client
    email_client = get_email_client()
    if not email_client:
        return "Error: Unable to initialize email client"
    
    try:
        # Create the email message with attachments
        logger.info(f"Creating email message with subject: {subject} and {len(attachments)} attachments")
        message = create_email_message_with_attachments(recipient, subject, content, attachments)
        
        # Send the email
        logger.info(f"Beginning email send operation with attachments")
        poller = email_client.begin_send(message)
        logger.info(f"Email send operation initiated, waiting for result")
        result = poller.result()
        
        return process_email_result(result, recipient)
    except Exception as e:
        logger.error(f"Failed to send email with attachments: {str(e)}", exc_info=True)
        return f"Failed to send email with attachments: {str(e)}"

def create_email_message_with_attachments(recipient: str, subject: str, content: str, attachments: list) -> Dict[str, Any]:
    """Create an email message with attachments for Azure Communication Services"""
    import base64
    
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
        "senderAddress": ACS_SENDER_ADDRESS,
        "attachments": []
    }
    
    for file_path in attachments:
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
                filename = os.path.basename(file_path)
                
                # Base64 encode the file content
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                
                # Add attachment to message
                message["attachments"].append({
                    "name": filename,
                    "contentType": "application/octet-stream",
                    "contentInBase64": encoded_content
                })
                
                logger.info(f"Added attachment: {filename}")
        except Exception as e:
            logger.warning(f"Failed to add attachment {file_path}: {str(e)}")
    
    return message

@mcp.tool(name="send_bulk_email")
def send_bulk_email(recipients: list, subject: str, content: str) -> str:
    """Send email to multiple recipients using Azure Communication Services
    
    Args:
        recipients: List of email addresses to send to
        subject: Subject line of the email
        content: HTML content of the email
        
    Returns:
        A message indicating the status of the email sending operation
    """
    logger.info(f"Starting bulk email sending process to {len(recipients)} recipients")
    
    # Validate configuration
    if not validate_config():
        return "Error: Email service is not configured properly. Check your .env file."
    
    # Get email client
    email_client = get_email_client()
    if not email_client:
        return "Error: Unable to initialize email client"
    
    success_count = 0
    failed_recipients = []
    
    try:
        # Create the email message for multiple recipients
        logger.info(f"Creating bulk email message with subject: {subject}")
        message = create_bulk_email_message(recipients, subject, content)
        
        # Send the email
        logger.info(f"Beginning bulk email send operation")
        poller = email_client.begin_send(message)
        logger.info(f"Bulk email send operation initiated, waiting for result")
        result = poller.result()
        
        success_count = len(recipients)
        return f"Bulk email sent successfully to {success_count} recipients!"
    except Exception as e:
        logger.error(f"Failed to send bulk email: {str(e)}", exc_info=True)
        return f"Failed to send bulk email: {str(e)}"

def create_bulk_email_message(recipients: list, subject: str, content: str) -> Dict[str, Any]:
    """Create an email message for multiple recipients using Azure Communication Services"""
    to_list = []
    for recipient in recipients:
        to_list.append({
            "address": recipient,
            "displayName": "Email Recipient"
        })
    
    return {
        "content": {
            "subject": subject,
            "plainText": content,
            "html": content
        },
        "recipients": {
            "to": to_list
        },
        "senderAddress": ACS_SENDER_ADDRESS
    }



# DEFINE RESOURCES

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
    
# execute and return the stdio output
if __name__ == "__main__":
    # Validate configuration at startup
    if not validate_config():
        logger.warning("Starting with invalid configuration - email sending will fail")
    
    logger.info("Starting MCP server for ACS Email Sender")
    mcp.run(transport="stdio")