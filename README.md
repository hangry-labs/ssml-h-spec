# SSML-H Specification

This repository is the normative home of SSML-H, the Hangry Labs extension
profile for W3C Speech Synthesis Markup Language 1.1.

- **Current draft:** [SSML-H 1.0](specification.md)
- **Namespace:** `https://hangrylabs.app/ns/ssml-h/1.0`
- **Rendered overview:** [index.html](index.html)
- **Reference tools:** [`hangry-labs/ssml-h-tools`](https://github.com/hangry-labs/ssml-h-tools)

SSML-H keeps standard synthesis markup in the SSML document body and places
Hangry Labs extensions in standard `<metadata>`. Version 1.0 defines dynamic
voice declarations with explicit request or persistent-profile scope.

This is an independent Hangry Labs specification. It is based on W3C SSML 1.1
but is not a W3C Recommendation and is not endorsed by W3C.

## Repository structure

| Path | Purpose |
|---|---|
| `specification.md` | Normative specification source |
| `index.html` | Static namespace overview |
| `styles.css` | Self-contained overview styling |
| `CONTRIBUTING.md` | Proposal and change process |
| `LICENSE.md` | W3C Software and Document License (2023) |

## License

Copyright 2026 Hangry Labs. The specification and its static presentation are
licensed under the [W3C Software and Document License (2023)](LICENSE.md).
