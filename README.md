# Todo List MCP MCP Server

This is an auto-generated Model Context Protocol (MCP) server deployed on Vercel.

## Overview

This MCP server exposes configured APIs as tools that can be used by Claude and other AI models.

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

4. Run the server:
```bash
python app/mcp_server.py
```

## Deployment

This project is configured for deployment on Vercel. To deploy:

1. Push to your GitHub repository
2. The repository should be connected to Vercel
3. Vercel will automatically build and deploy on push

## Environment Variables

Set these in your Vercel project settings:
- `OPENAI_API_KEY`: Your OpenAI API key

## API Endpoints

The MCP server exposes the following endpoints:
- `/`: Health check
- `/health`: Server status

## Support

For issues or questions, contact your system administrator.
