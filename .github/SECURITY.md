# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | ✓         |

## Security Considerations

The MCP plugin opens a TCP server on `localhost:31337`. This interface:
- **Binds only to 127.0.0.1** — not accessible from other machines
- **No authentication** — any local process can connect
- **Plaintext JSON over TCP**

### Recommendations

- Run ImHex in an isolated environment (VM/container) when analyzing untrusted binaries
- Block port 31337 from external networks via firewall
- Limit ImHex's file system permissions
- Use OS-level resource limits (`ulimit`, cgroups)

## Reporting a Vulnerability

Create a private issue on GitHub with title `SECURITY: <brief description>`. Provide details on the vulnerability type, reproduction steps, and potential impact.

## Response Timeline

- **Acknowledgment:** Within 48 hours
- **Assessment:** Within 1 week
- **Fix:** Based on severity (critical: 7 days, high: 14 days, medium: 30 days)
- **Disclosure:** After fix is released

## Known Limitations

1. **No authentication** — mitigated by localhost-only binding
2. **No encryption** — mitigated by localhost-only binding
3. **Full file system access** — mitigate by running with minimal OS privileges
