from __future__ import annotations

from datetime import timedelta

DOMAIN = "wink_local"
PLATFORMS = ["light", "switch", "lock", "binary_sensor", "sensor", "button", "event"]
DEFAULT_PORT = 8888
DEFAULT_SCAN_INTERVAL = 15
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_USER = "root"
CONF_TOKEN = "token"
CONF_VERIFY_SSL = "verify_ssl"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_SSH_ENABLED = "ssh_enabled"
CONF_SSH_PORT = "ssh_port"
CONF_SSH_USER = "ssh_user"
CONF_SSH_PASSWORD = "ssh_password"
CONF_SSH_PRIVATE_KEY = "ssh_private_key"
ATTR_RADIO = "radio"
ATTR_TIMEOUT = "timeout"
ATTR_MASTER_ID = "master_id"
ATTR_FORCE = "force"
ATTR_NAME = "name"
ATTR_SCENE = "scene"
SUPPORTED_RADIOS = ("zigbee", "zwave", "lutron", "kidde", "http")
UPDATE_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
