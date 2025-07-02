
import httpx, sys
import json
import logging
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Apstra MCP server 6.0.0")

# IP of Cloudlabs AOS Server
aos_server = 'apstra-7f840a14-99fe-4740-96dc-6a74ee018213.aws.apstra.com'
username = 'admin'
password = 'InventiveFox9$'
def auth():
    try:
        url_login = f'https://{aos_server}/api/user/login'
        headers_init = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        data = json.dumps({
            "username": username,
            "password": password
        })
        response = httpx.post(url_login, data=data, headers=headers_init, verify=False)
        if response.status_code != 201:
            sys.exit('error: authentication failed')
        auth_token = response.json()['token']
        headers = {
            'AuthToken': auth_token,
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        #print("Authentication successful. " + headers['AuthToken'])
        return headers
        
    except Exception as e:
        logging.error(f"Auth error: {e}")
        return {}
    
    # Get blueprints
@mcp.tool()
def get_bp() -> str:
    """Gets blueprint information"""
    try:
        headers = auth()
        url = f'https://{aos_server}/api/blueprints'
        response = httpx.get(url, headers=headers, verify=False)
        return json.dumps(response.json()['items'])
    except Exception as e:
        logging.error(f"get_bp error: {e}")
        return json.dumps({"error": str(e)})

# Get racks
@mcp.tool()
def get_racks(blueprint_id) -> str:
    """Gets rack information for a blueprint"""
    try:
        headers = auth()
        url = f'https://{aos_server}/api/blueprints/{blueprint_id}/racks'
        response = httpx.get(url, headers=headers, verify=False)
        return json.dumps(response.json()['items'])
    except Exception as e:
        logging.error(f"get_racks error: {e}")
        return json.dumps({"error": str(e)})

# Get routing zones
@mcp.tool()
def get_rz(blueprint_id) -> str:
    """Gets routing zone information for a blueprint"""
    try:
        headers = auth()
        url = f'https://{aos_server}/api/blueprints/{blueprint_id}/security-zones'
        response = httpx.get(url, headers=headers, verify=False)
        return json.dumps(response.json())
    except Exception as e:
        logging.error(f"get_rz error: {e}")
        return json.dumps({"error": str(e)})

# Create virtual networks
@mcp.tool()
def create_vn(blueprint_id, security_zone_id, vn_name) -> str:
    """Creates a virtual network in a given blueprint and routing zone"""
    try:
        headers = auth()
        url = f'https://{aos_server}/api/blueprints/{blueprint_id}/virtual-networks'
        data = json.dumps({
            "label": vn_name,
            "vn_type": "vxlan",
            "security_zone_id": security_zone_id
        })
        response = httpx.post(url, data=data, headers=headers, verify=False)
        return json.dumps(response.json())
    except Exception as e:
        logging.error(f"create_vn error: {e}")
        return json.dumps({"error": str(e)})

# Check staging version through diff-status
@mcp.tool()
def get_diff_status(blueprint_id) -> str:
    """Gets the diff status for a blueprint"""
    try:
        headers = auth()
        url = f'https://{aos_server}/api/blueprints/{blueprint_id}/diff-status'
        response = httpx.get(url, headers=headers, verify=False)
        return json.dumps(response.json())
    except Exception as e:
        logging.error(f"get_diff_status error: {e}")
        return json.dumps({"error": str(e)})

# Deploy config
@mcp.tool()
def deploy(blueprint_id: str, description: str, staging_version: int) -> str:
    """Deploys the config for a blueprint"""
    try:
        headers = auth()
        url = f'https://{aos_server}/api/blueprints/{blueprint_id}/deploy'
        data = json.dumps({
            "version": staging_version,
            "description": description
        })
        response = httpx.put(url, headers=headers, data=data, verify=False)
        return json.dumps(response.json())
    except Exception as e:
        logging.error(f"deploy error: {e}")
        return json.dumps({"error": str(e)})
