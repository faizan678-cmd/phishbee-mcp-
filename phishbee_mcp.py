from mcp.server.fastmcp import FastMCP
import httpx
import os
import uvicorn

mcp = FastMCP("PhishBee")

PHISHBEE_URL = "https://phishbee-io.up.railway.app"

@mcp.tool()
async def check_url(url: str) -> str:
    """Check if a URL is phishing or safe using PhishBee."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{PHISHBEE_URL}/api/check-url/",
                json={"url": url}
            )
            data = response.json()
            return f"URL: {data['url']}\nVerdict: {data['verdict']}\nScore: {data['score']}\nReasons: {', '.join(data['reasons'])}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=port,
        forwarded_allow_ips="*",
        proxy_headers=True
    )
