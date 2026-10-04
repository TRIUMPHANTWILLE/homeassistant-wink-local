# Wink Local 0.5.0

A Home Assistant custom integration for a rooted Wink Hub 1 using the hub's local AAU HTTPS API for discovery and normal control, plus optional SSH access for radio management.

## Status

Verified against a rooted Wink Hub 1 with AAU local-control server 2.6.0 and an IKEA TRADFRI E26 1000 lm Zigbee bulb. Zigbee discovery, on/off state, brightness state, pairing, and direct `aprontest` control were verified. Z-Wave, Lutron, Kidde, HTTP-backed devices, scenes, and AAU PUT control are implemented as experimental paths and require device testing.

## Installation

1. Copy `custom_components/wink_local` into Home Assistant's `/config/custom_components/` directory.
2. Restart Home Assistant.
3. Open Settings > Devices & services > Add integration.
4. Search for `Wink Local`.
5. Enter the hub host, AAU token, and optional SSH settings.

## Required hub preparation

- Rooted Wink Hub 1
- AAU server reachable on TCP 8888
- A valid local-control bearer token
- Optional SSH access for pairing, exclusion, refresh, rename, and removal

The stock AAU code considers token data expired after seven days. This integration detects `401 tokens expired` and reports a clear authentication error, but does not modify the hub automatically.

## Supported actions

- `wink_local.start_pairing`
- `wink_local.start_exclusion`
- `wink_local.refresh_device`
- `wink_local.reconfigure_device`
- `wink_local.rename_device`
- `wink_local.remove_device`
- `wink_local.run_scene`

## Example pairing action

```yaml
action: wink_local.start_pairing
data:
  radio: zigbee
  timeout: 60
```

## Design notes

The Wink Zigbee and Z-Wave radios remain separate coordinator networks. Devices paired through Wink do not join an existing ZHA, Zigbee2MQTT, or Z-Wave JS network. Home Assistant controls them through this integration.

## Security

Keep TCP 8888 and SSH restricted to the local network. Prefer an SSH key. The integration redacts tokens and passwords from diagnostics.
