# MCP Server with Azure Communication Services Email

This is a Model Context Protocol (MCP) server with Azure Communication Services email functionality.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your environment variables by creating a `.env` file in the root directory with the following variables:
```
ACS_CONNECTION_STRING=your_azure_communication_services_connection_string
ACS_SENDER_ADDRESS=your_verified_sender_address@your-domain.azurecomm.net
```

## Azure Communication Services Setup

To use the email functionality, you need to:

1. Create an Azure Communication Services resource in the Azure Portal
2. Configure Email Communication Services
3. Verify a domain for sending emails
4. Get your connection string from the Azure Portal

## Running the server

```bash
python src/server.py
```

## Available Tools

The server provides the following tools:

- `send_email`: Send emails using Azure Communication Services
- Various math operations: add, subtract, multiply, divide, etc.
- `calculate_bmi`: Calculate Body Mass Index

## Usage Examples

### Send an Email
```
email://recipient@example.com?subject=Test%20Email&content=Hello%20World
```

### Get a Greeting
```
greeting://YourName
