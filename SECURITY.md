# Security Policy

Specification issues that could cause unsafe parser behavior, remote resource
access, profile replacement, data exposure, or unbounded resource use should
be reported privately through GitHub's security advisory interface.

Implementation-specific vulnerabilities belong in the affected processor or
tool repository. The SSML-H specification does not permit DTDs, entities,
external references, remote audio, external lexicons, or generic network
access in version 1.0. Voice descriptions and per-turn directions are untrusted
plain text and must never be interpreted as code, paths, URLs, templates, or
authorization policy.
