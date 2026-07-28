---
name: Patch Failure
about: Report patches failing to apply to ImHex
title: '[PATCH] Patch fails to apply'
labels: patch-failure
assignees: ''
---

## Patch Information

**Which patch failed?**
- [ ] 01-builtin-library-plugin
- [ ] 02-fileprovider-public-open
- [ ] 03-fileprovider-graceful-settings
- [ ] 04-provider-graceful-settings
- [ ] 05-appleclang-build-helpers
- [ ] 06-mcp-api-compatibility
- [ ] 07-enable-network-interface

## ImHex Version

**Commit hash:**
```
cd ImHex && git rev-parse HEAD
```

**Branch:**
- [ ] master
- [ ] nightly
- [ ] Other: ___________

## Error Output

```
Paste the error output from git apply
```

## Steps Taken

1. Cloned ImHex: `git clone https://github.com/WerWolv/ImHex.git`
2. Applied patches: `cd ImHex && git apply ../patches/*.patch`
