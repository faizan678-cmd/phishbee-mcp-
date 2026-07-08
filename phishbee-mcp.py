from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("PhishBee")

PHISHBEE_URL = "https://phishbee.up.railway.app"

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
    mcp.run(transport="streamable-http")
