# TODO

## Pending Bug Fixes

### `memory-advice` in config.json

**Status:** ⏳ Waiting for ASUSTOR support fix

**Description:**  
The `memory-advice` field in `apk/CONTROL/config.json` has been temporarily removed due to a bug in ASUSTOR's App Central.

**Original value to restore:**
```json
"memory-advice": 8192,
```

**Location:** After `"memory-limit": 4096,` in `apk/CONTROL/config.json`

**Action required:**  
Once ASUSTOR support confirms the bug is fixed, add the line back:

```json
"firmware": "5.1.0",
"default-lang": "en-US",
"memory-limit": 4096,
"memory-advice": 8192,
"privacy-statement": "https://runtipi.io/docs/reference/privacy-policy",
```

**Reported:** December 2025  
**Ticket/Reference:** ASUSTOR Support #91706

---

_This file tracks temporary workarounds and pending fixes._
