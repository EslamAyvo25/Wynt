from fastapi import FastAPI, Request, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# Define a list of trusted IP addresses (whitelist)
TRUSTED_IPS = ["127.0.0.1", "192.168.1.100"]

# Define a valid API key for access
API_KEY = "mysecretapikey"
API_KEY_NAME = "access-token"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

# Function to check the client IP address
def check_ip_whitelist(request: Request):
    client_ip = request.client.host
    if client_ip not in TRUSTED_IPS:
        raise HTTPException(status_code=403, detail="Access forbidden: Unauthorized IP")

# Function to check API key
async def check_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Protected endpoint with IP whitelist and API key validation
@app.get("/protected-endpoint")
async def protected_endpoint(request: Request, api_key: str = Security(check_api_key)):
    # Check if client IP is in whitelist
    check_ip_whitelist(request)
    return {"OK"}
