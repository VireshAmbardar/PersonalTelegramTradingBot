
import time
import hmac
from hashlib import sha256
from typing import Dict, Any
import requests
import os
from dotenv import load_dotenv
load_dotenv()
import json

api_key = os.environ.get('BINGX_API_KEY', '')
secret_key = os.environ.get('BINGX_SECRET_KEY', '')
global listening_key

__all__ = [
    "generate_listen_key",
    "extend_listen_key",
]

# Base URL for the BingX open API.  You can override this if needed (e.g. for
# testing against a sandbox environment).
APIURL = "https://open-api.bingx.com"





def _parse_param(params: Dict[str, Any]) -> str:
    """Build a query string from a dict of parameters and append the required timestamp.

    The BingX API requires a millisecond‐precision `timestamp` on signed
    requests.  This helper ensures the timestamp is always present.  If any
    other parameters are provided, they are sorted alphabetically as required
    by the signing rules.

    Args:
        params: A mapping of parameter names to values.

    Returns:
        A query string with the form `key1=value1&key2=value2&timestamp=...`.
    """
    # Sort parameter keys alphabetically
    sorted_keys = sorted(params)
    # Build the base string of parameters
    param_str = "&".join([f"{key}={params[key]}" for key in sorted_keys])
    # Append the timestamp (in milliseconds)
    timestamp = str(int(time.time() * 1000))
    if param_str:
        return f"{param_str}&timestamp={timestamp}"
    else:
        return f"timestamp={timestamp}"


def _get_sign(secret_key: str, payload: str) -> str:
    """Compute the HMAC SHA-256 signature of a payload string.

    Args:
        secret_key: Your BingX API secret.
        payload: The string to sign (typically the query string).

    Returns:
        Hexadecimal digest of the HMAC signature.
    """
    return hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()


def _send_request(api_key: str, secret_key: str, method: str, path: str, params: Dict[str, Any], payload: Dict[str, Any], key:str) -> str:
    """Send an authenticated request to the BingX API.

    This helper assembles the full URL with query parameters, computes the
    signature, attaches the API key header, and performs the HTTP request.

    Args:
        api_key: Your BingX API key.
        secret_key: Your BingX API secret key.
        method: HTTP method ("POST" or "PUT").
        path: Endpoint path (e.g. '/openApi/user/auth/userDataStream').
        params: Dictionary of query parameters (without timestamp).
        payload: Request body payload (for BingX listen key operations this is
            typically empty).

    Returns:
        The response text returned by the BingX API.
    """
    # Build the query string with timestamp
    param_str = _parse_param(params)
    # Compute signature using the secret key and the query string
    signature = _get_sign(secret_key, param_str)
    # Construct the full request URL
    url = f"{APIURL}{path}?{param_str}&signature={signature}"
    
    if method == 'PUT':
        print("Listening Key :",key)
        headers = {"listenKey": key}
    else:
        headers = {'X-BX-APIKEY': api_key}
    response = requests.request(method, url, headers=headers, data=payload)
    response.raise_for_status()
    return response.text


def generate_listen_key() -> str:
    """Generate a new listen key for the user data stream.

    This performs an HTTP `POST` to `/openApi/user/auth/userDataStream` as
    documented in the BingX API specification.  You need to call this
    function once before using a websocket to receive account and order
    updates.

    Args:
        api_key: Your BingX API key.
        secret_key: Your BingX API secret key.

    Returns:
        The raw response text containing the listen key (usually JSON).
    """
    path = '/openApi/user/auth/userDataStream'
    method = 'POST'
    params = {}
    payload = {}
    data = json.loads(_send_request(api_key, secret_key, method, path, params, payload, None))
    return data['listenKey']


def extend_listen_key(key:str) -> str:
    """Extend the validity period of an existing listen key.

    To prevent your websocket connection from being invalidated, you must
    periodically call this endpoint before the current listen key expires.
    This performs an HTTP `PUT` request to the same endpoint used for
    generation.

    Args:
        api_key: Your BingX API key.
        secret_key: Your BingX API secret key.

    Returns:
        The raw response text from the API.  The response format is the same
        as the generate operation.
    """
    path = '/openApi/user/auth/userDataStream'
    method = 'PUT'
    params = {}
    payload = {}
    return _send_request(api_key, secret_key, method, path, params, payload, key)


if __name__ == '__main__':  # pragma: no cover
#     # Simple demonstration when running this module directly
#     import os
#     from dotenv import load_dotenv
#     load_dotenv()
#     APIKEY_ENV = os.environ.get('BINGX_API_KEY', '')
#     SECRETKEY_ENV = os.environ.get('BINGX_SECRET_KEY', '')
#     if not APIKEY_ENV or not SECRETKEY_ENV:
#         print("Please set BINGX_APIKEY and BINGX_SECRETKEY environment variables to test.")
#     else:
#         print("Generating listen key...")
    gen_resp = generate_listen_key()
    
    # print(gen_resp, type(gen_resp))
    # print("Extending listen key...")
    # listening_key = gen_resp
    ext_resp = extend_listen_key(gen_resp)
    print(ext_resp)