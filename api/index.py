"""Vercel serverless handler for MCP server."""
import os
import sys

# Add the app directory to sys.path so we can import mcp_server

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

try:
    from mcp_server import mcp

    # Expose the Starlette app for Vercel
    # FastMCP uses Starlette internally. 
    # We need to access the underlying app.
    if hasattr(mcp, 'sse_app'):
        app = mcp.sse_app()
    elif hasattr(mcp, '_sse_app'):
        app = mcp._sse_app
    elif hasattr(mcp, 'app'):
        app = mcp.app
    else:
        # Fallback: try to create an app if FastMCP doesn't expose it directly
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import JSONResponse
        
        async def health(request):
            return JSONResponse({"status": "error", "message": "Could not find MCP app instance"})
            
        app = Starlette(routes=[Route("/", health)])

except Exception as e:
    # Catch initialization errors and return them
    import traceback
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    
    error_msg = f"Initialization Error: {str(e)}\n{traceback.format_exc()}"
    
    async def error_handler(request):
        return JSONResponse({
            "status": "error", 
            "message": "Server failed to start", 
            "details": error_msg
        }, status_code=500)
        
    app = Starlette(routes=[Route("/{path:path}", error_handler)])
