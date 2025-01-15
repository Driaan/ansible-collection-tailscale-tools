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