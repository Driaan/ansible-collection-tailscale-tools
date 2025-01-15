from __future__ import absolute_import, division, print_function

__metaclass__ = type

import requests
import json
from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.module_utils._text import to_text

DOCUMENTATION = """
---
name: tailscale_inventory
plugin_type: inventory
short_description: Retrieves Tailscale nodes as dynamic inventory.
description:
    - Queries the Tailscale API to retrieve device information for a tailnet.
options:
    plugin:
        description: The name of the plugin.
        required: true
        choices: ['driaan.tailscale_tools.tailscale_inventory']
    api_key:
        description: Your Tailscale API access token.
        required: false
        type: str
    oauth_client_id:
        description: OAuth Client ID for obtaining access tokens.
        required: false
        type: str
    oauth_client_secret:
        description: OAuth Client Secret for obtaining access tokens.
        required: false
        type: str
    tailnet_name:
        description: Tailnet name to query devices.
        required: false
        type: str
        default: "-"
"""

EXAMPLES = """
plugin: driaan.tailscale_tools.tailscale_inventory
api_key: "your_tailscale_api_key"
tailnet_name: "example.com"
"""


class InventoryModule(BaseInventoryPlugin):
    NAME = "driaan.tailscale_tools.tailscale_inventory"

    def verify_file(self, path):
        return super(InventoryModule, self).verify_file(path) and path.endswith(".yaml")

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        config = self._read_config_data(path)
        api_key = config.get("api_key")
        oauth_client_id = config.get("oauth_client_id")
        oauth_client_secret = config.get("oauth_client_secret")
        tailnet_name = config.get("tailnet_name", "-")

        if not api_key and (not oauth_client_id or not oauth_client_secret):
            raise AnsibleError(
                "Either 'api_key' or both 'oauth_client_id' and 'oauth_client_secret' must be provided."
            )

        # Get access token if using OAuth
        if not api_key:
            api_key = self._get_oauth_token(oauth_client_id, oauth_client_secret)

        headers = {"Authorization": f"Bearer {api_key}"}
        url = f"https://api.tailscale.com/api/v2/tailnet/{tailnet_name}/devices"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            for node in data.get("devices", []):
                self.inventory.add_host(node["hostname"])
                self.inventory.set_variable(
                    node["hostname"], "ip", node["addresses"][0]
                )
                self.inventory.set_variable(
                    node["hostname"], "tags", node.get("tags", [])
                )

        except requests.exceptions.RequestException as e:
            raise AnsibleError(f"Failed to query Tailscale API: {to_text(e)}")

    def _get_oauth_token(self, client_id, client_secret):
        """Get an access token using OAuth client credentials."""
        token_url = "https://api.tailscale.com/api/v2/oauth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_info = response.json()
            return token_info.get("access_token")
        except requests.exceptions.RequestException as e:
            raise AnsibleError(f"Failed to retrieve OAuth token: {to_text(e)}")
