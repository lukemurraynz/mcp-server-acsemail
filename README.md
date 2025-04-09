# MCP Server with Azure Communication Services Email

This is a Model Context Protocol (MCP) server with Azure Communication Services email functionality. It allows you to send emails programmatically and perform various operations.

Blog: [Sending Emails with MCP and Azure Communication Services](https://luke.geek.nz/azure/mcp-acs-email-integration/)

## Prerequisites

- Python 3.8 or higher
- Azure Communication Services resource with email capabilities configured
- Verified sender email address in Azure Communication Services

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

1. Create an Azure Communication Services resource in the Azure Portal.
2. Configure Email Communication Services.
3. Verify a domain for sending emails.
4. Get your connection string from the Azure Portal.

## Running the Server

Start the server by running the following command:
```bash
python src/server.py
```

## Directory Structure

```
/workspaces/mcp-server-acsemail
├── README.md
├── requirements.txt
├── src/
│   └── server.py
```

- `README.md`: Documentation for the project.
- `requirements.txt`: Python dependencies.
- `src/server.py`: Main server script.

## Features

The server provides the following tools and functionalities:

- **Email Sending**: Send emails using Azure Communication Services.

## Example Usage

Here is an example of how to send an email using the server:

1. Start the server:
```bash
python src/server.py
```

2. Prompt to send email

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request for review.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
