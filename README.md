# Tailscale Tools Ansible Collection

This collection provides a dynamic inventory plugin for integrating Tailscale with Ansible.

## Requirements
- Python `tailscale` module installed
- Tailscale API key with proper permissions

## Usage
1. Configure your inventory:
   ```yaml
   plugin: driaan.tailscale_tools.tailscale_inventory
   api_key: "your_tailscale_api_key"
    ```

2. Run your playbook:
   ```shell
   ansible-playbook -i tailscale_inventory.yml playbook.yml
   ```